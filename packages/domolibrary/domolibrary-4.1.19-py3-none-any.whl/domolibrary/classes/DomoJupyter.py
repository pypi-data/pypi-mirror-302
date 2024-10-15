# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoJupyter.ipynb.

# %% auto 0
__all__ = ['DomoJupyterWorkspace_Content', 'DomoJupyterDataSource', 'DomoJupyterAccount', 'DomoJupyterWorkspace',
           'get_jupyter_workspaces', 'search_workspace_by_name', 'DomoJupyter_InvalidWorkspace']

# %% ../../nbs/classes/50_DomoJupyter.ipynb 2
from ..routes.jupyter import JupyterAPI_Error

# %% ../../nbs/classes/50_DomoJupyter.ipynb 3
import os
import json

from dataclasses import dataclass, field
from typing import List
import datetime as dt

import httpx

import domolibrary.utils.DictDot as util_dd
from dateutil.parser import parse

import domolibrary.client.DomoAuth as dmda
import domolibrary.routes.jupyter as jupyter_routes
import domolibrary.classes.DomoAccount as dmacc
import domolibrary.classes.DomoDataset as dmds
import domolibrary.classes.DomoUser as dmdu


import domolibrary.client.DomoError as de
import domolibrary.utils.chunk_execution as ce

from nbdev.showdoc import patch_to

# %% ../../nbs/classes/50_DomoJupyter.ipynb 7
@dataclass
class DomoJupyterWorkspace_Content:
    name: str
    folder: str
    last_modified: dt.datetime
    file_type: str
    content: str

    auth: dmda.DomoJupyterAuth = field(repr=False)

    default_export_folder: str = "export"

    def __post_init__(self):
        dmda.test_is_jupyter_auth(self.auth)

        if self.folder.endswith(self.name):
            self.folder = self.folder.replace(self.name, "")

    @classmethod
    def _from_json(cls, obj: dict, auth: dmda.DomoJupyterAuth):
        dd = util_dd.DictDot(obj) if not isinstance(obj, util_dd.DictDot) else obj

        dc = cls(
            name=dd.name,
            folder=dd.path,
            last_modified=parse(dd.last_modified),
            file_type=dd.type,
            auth=auth,
            content=obj.get("content"),
        )

        return dc

    def export(
        self,
        output_folder: str = None,
        file_name: str = None,
        default_export_folder: str = None,
    ):
        if default_export_folder:
            self.default_export_folder = default_export_folder

        output_folder = output_folder or os.path.join(
            self.default_export_folder, self.folder
        )

        file_name = file_name or self.name

        if not os.path.exists(output_folder):
            print(output_folder)
            os.makedirs(output_folder)

        content_str = self.content
        if isinstance(self.content, dict):

            content_str = json.dumps(self.content)

        output_path = os.path.join(output_folder, file_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content_str)
            f.close()

        return output_path

    async def update(
        self,
        jupyter_folder: str = None,
        jupyter_file_name: str = None,
        debug_api: bool = False,
    ):
        if jupyter_folder and jupyter_file_name:
            content_path = f"{jupyter_folder}/{jupyter_file_name}"

        if len(self.folder) > 0:
            content_path = f"{self.folder}/{self.name}"

        else:
            content_path = self.name

            if content_path.lower().startswith(self.default_export_folder.lower()):
                content_path = content_path.replace(self.default_export_folder, "")

        content_path = "/".join(os.path.normpath(content_path).split(os.sep))

        return await jupyter_routes.update_jupyter_file(
            auth=self.auth,
            content_path=content_path,
            new_content=self.content,
            debug_api=debug_api,
            debug_num_stacks_to_drop=2,
            parent_class=self.__class__.__name__,
        )

# %% ../../nbs/classes/50_DomoJupyter.ipynb 9
@dataclass
class DomoJupyterDataSource:
    datasource_id: str
    alias: str

    def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False

        return self.datasource_id == other.datasource_id

    @classmethod
    def _from_json(cls, obj):
        return cls(datasource_id=obj["dataSourceId"], alias=obj["alias"])

    def to_json(self):
        return {"dataSourceId": self.datasource_id, "alias": self.alias}


@dataclass
class DomoJupyterAccount:
    account_id: str
    alias: str

    def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False

        return self.account_id == other.account_id

    @classmethod
    def _from_json(cls, obj):
        return cls(account_id=obj["account_id"], alias=obj["alias"])

    def to_json(self):
        return {"account_id": self.account_id, "alias": self.alias}


@dataclass
class DomoJupyterWorkspace:
    auth: dmda.DomoJupyterAuth = field(repr=False)
    id: str
    name: str
    description: str

    created_dt: dt.datetime
    updated_dt: dt.datetime

    owner: dict
    cpu: str
    memory: int

    last_run_dt: dt.datetime = None
    instances: List[dict] = None
    input_configuration: List[DomoJupyterDataSource] = field(default_factory= lambda : [])
    output_configuration: List[DomoJupyterDataSource] = field(default_factory= lambda : [])
    account_configuration: List[DomoJupyterAccount] = field(default_factory= lambda : [])
    collection_configuration: List[dict] = None
    fileshare_configuration: List[dict] = None

    content: List[DomoJupyterWorkspace_Content] = field(default=None)

    jupyter_token: str = None
    service_location: str = None
    service_prefix: str = None

    def __post_init__(self):
        self._update_auth_params()

    def _update_auth_params(self):
        if self.instances:
            res = jupyter_routes.parse_instance_service_location_and_prefix(
                self.instances[0], self.auth.domo_instance
            )
            self.service_location = res["service_location"]
            self.service_prefix = res["service_prefix"]

        if self.service_location and self.service_prefix and self.jupyter_token:
            self.update_auth()

    def update_auth(
        self, service_location=None, service_prefix=None, jupyter_token=None
    ):

        self.service_location = service_location or self.service_location
        self.service_prefix = service_prefix or self.service_prefix
        self.jupyter_token = jupyter_token or self.jupyter_token

        if isinstance(self.auth, dmda.DomoFullAuth):
            self.auth = dmda.DomoJupyterFullAuth.convert_auth(
                auth=self.auth,
                service_location=self.service_location,
                jupyter_token=self.jupyter_token,
                service_prefix=self.service_prefix,
            )

        if isinstance(self.auth, dmda.DomoTokenAuth):
            self.auth = dmda.DomoJupyterTokenAuth.convert_auth(
                auth=self.auth,
                service_location=self.service_location,
                jupyter_token=self.jupyter_token,
                service_prefix=self.service_prefix,
            )

        self.auth.service_location = self.service_location
        self.auth.service_prefix = self.service_prefix
        self.auth.jupyter_token = self.jupyter_token

    @classmethod
    def _from_json(
        cls,
        obj,
        auth,
        jupyter_token: str = None,
    ):

        output_configuration = (
            [
                DomoJupyterDataSource._from_json(obj=oc)
                for oc in obj["outputConfiguration"]
            ]
            if obj["outputConfiguration"]
            else []
        )
        input_configuration = (
            [DomoJupyterDataSource._from_json(ic) for ic in obj["inputConfiguration"]]
            if obj["inputConfiguration"]
            else []
        )
        account_configuration = (
            [DomoJupyterAccount._from_json(ac) for ac in obj["accountConfiguration"]]
            if obj["accountConfiguration"]
            else []
        )

        domo_workspace = cls(
            auth=auth,
            id=obj["id"],
            name=obj["name"],
            description=obj["description"],
            created_dt=obj["created"],
            updated_dt=obj["updated"],
            last_run_dt=obj.get("lastRun"),
            instances=obj["instances"],
            owner = obj['owner'],
            memory=obj["memory"],
            cpu=obj["cpu"],
            input_configuration=input_configuration,
            output_configuration=output_configuration,
            account_configuration=account_configuration,
            fileshare_configuration=obj["collectionConfiguration"],
            jupyter_token=jupyter_token,
        )
        return domo_workspace

    def _add_config(self, config, attribute):

        config_ls = getattr(self, attribute)

        if config not in config_ls:
            config_ls.append(config)

    def add_config_input_datasource(self, input_datasource: DomoJupyterDataSource):
        self._add_config(input_datasource, attribute="input_configuration")

    def add_config_output_datasource(self, input_datasource: DomoJupyterDataSource):
        self._add_config(input_datasource, attribute="output_configuration")

    def add_config_account(self, account: DomoJupyterAccount):
        self._add_config(account, attribute="account_configuration")


    def to_json(self):

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "memory": int(self.memory),
            "cpu": self.cpu,
            "inputConfiguration": [
                confg.to_json() for confg in self.input_configuration or []
            ],
            "outputConfiguration": [
                confg.to_json() for confg in self.output_configuration or []
            ],
            "accountConfiguration": [
                confg.to_json() for confg in self.account_configuration or []
            ],
            "fileshareConfiguration": self.collection_configuration or [],
        }

# %% ../../nbs/classes/50_DomoJupyter.ipynb 10
@patch_to(DomoJupyterWorkspace, cls_method=True)
async def get_by_id(
    cls,
    workspace_id,
    auth: dmda.DomoAuth,  # this API does not require the jupyter_token, but activities inside the workspace will require additional authentication
    jupyter_token=None,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):

    res = await jupyter_routes.get_jupyter_workspace_by_id(
        workspace_id=workspace_id,
        auth=auth,
        session=session,
        debug_api=debug_api,
        parent_class=cls.__name__,
    )

    if return_raw:
        return res

    return cls._from_json(auth=auth, obj=res.response, jupyter_token=jupyter_token)

# %% ../../nbs/classes/50_DomoJupyter.ipynb 11
async def get_jupyter_workspaces(
    auth: dmda.DomoAuth,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    return_raw : bool = False
):
    res = await jupyter_routes.get_jupyter_workspaces(
        auth=auth,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    return await ce.gather_with_concurrency(
        *[
            DomoJupyterWorkspace.get_by_id(
                auth=auth,
                workspace_id=workspace["id"],
                debug_api=debug_api,
                session=session,
            )
            for workspace in res.response
        ],
        n=10,
    )


async def search_workspace_by_name(
    workspace_name: str,
    auth: dmda.DomoAuth,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    return_raw: bool = False,
):
    res = await get_jupyter_workspaces(
        auth=auth,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        return_raw=return_raw,
    )

    workspace = None
    if return_raw:
        workspace = next(
            (
                workspace
                for workspace in res.response
                if workspace["name"] == workspace_name
            ),
            None,
        )
        res.response = workspace

    else:
        workspace = next(
            (workspace for workspace in res if workspace.name == workspace_name),
            None,
        )

    if not workspace:
        raise jupyter_routes.JupyterAPI_Error(
            status=200,
            domo_instance=auth.domo_instance,
            response=f"unable to find workspace with name {workspace_name}",
        )

    return res if return_raw else workspace

# %% ../../nbs/classes/50_DomoJupyter.ipynb 14
@patch_to(DomoJupyterWorkspace)
async def update_config(
    self,
    config: dict = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
):
    config = config or self.to_json()

    return await jupyter_routes.update_jupyter_workspace_config(
        auth=self.auth,
        workspace_id=self.id,
        config=config,
        parent_class=self.__class__.__name__,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )


@patch_to(DomoJupyterWorkspace)
async def add_account(
    self,
    domo_account: dmacc.DomoAccount,
    domo_user: dmdu.DomoUser = None,
    update_config: bool = True,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    dja = DomoJupyterAccount(
        alias=domo_account.name, account_id=domo_account.id
    )

    self.add_config_account(dja)

    if not update_config:
        return self.account_configuration

    share_user_id = (domo_user and domo_user.id) or (
        await self.auth.who_am_i()
    ).response["id"]

    retry = 0
    while retry <= 1:
        try:
            return await self.update_config(debug_api=debug_api, session=session)

        except JupyterAPI_Error as e:
            await domo_account._share_v2(
                user_id=share_user_id,
                auth=self.auth,
                # is_v2 = True,
                debug_api=debug_api,
                session=session,
            )

            retry += 1


@patch_to(DomoJupyterWorkspace)
async def add_input_dataset(
    self,
    domo_dataset: dmds.DomoDataset,
    domo_user: dmdu.DomoUser = None,
    update_config: bool = True,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    djds = DomoJupyterDataSource(alias=domo_dataset.name, datasource_id=domo_dataset.id)

    self.add_config_input_datasource(djds)

    if not update_config:
        return self.input_configuration

    domo_user = domo_user or await dmdu.DomoUser.get_by_id(
        auth=self.auth,
        user_id=(await self.auth.who_am_i()).response["id"],
        debug_api=debug_api,
        session=session,
    )

    retry = 0

    while retry <= 1:
        try:
            return await self.update_config(debug_api=debug_api, session=session)

        except JupyterAPI_Error as e:
            await domo_dataset.share(
                member=domo_user, auth=self.auth, debug_api=debug_api, session=session
            )

            retry += 1


@patch_to(DomoJupyterWorkspace)
async def add_output_dataset(
    self,
    domo_dataset: dmds.DomoDataset,
    domo_user: dmdu.DomoUser = None,
    update_config: bool = True,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    djds = DomoJupyterDataSource(alias=domo_dataset.name, datasource_id=domo_dataset.id)

    self.add_config_output_datasource(djds)

    if not update_config:
        return self.output_configuration

    domo_user = domo_user or await dmdu.DomoUser.get_by_id(
        auth=self.auth,
        user_id=(await self.auth.who_am_i()).response["id"],
        debug_api=debug_api,
        session=session,
    )

    retry = 0

    while retry <= 1:
        try:
            return await self.update_config(debug_api=debug_api, session=session)

        except JupyterAPI_Error as e:
            await domo_dataset.share(
                member=domo_user, auth=self.auth, debug_api=debug_api, session=session
            )

            retry += 1

# %% ../../nbs/classes/50_DomoJupyter.ipynb 15
@patch_to(DomoJupyterWorkspace)
async def get_content(
    self,
    debug_api: bool = False,
    return_raw: bool = False,
    is_recursive: bool = True,
    content_path: str = "",
):
    res = await jupyter_routes.get_content(
        auth=self.auth,
        debug_api=debug_api,
        content_path=content_path,
        debug_num_stacks_to_drop=2,
        parent_class=self.__class__.__name__,
        is_recursive=is_recursive,
        return_raw=return_raw,
    )

    if return_raw:
        return res

    return [
        DomoJupyterWorkspace_Content._from_json(obj, auth=self.auth)
        for obj in res.response
    ]

# %% ../../nbs/classes/50_DomoJupyter.ipynb 22
class DomoJupyter_InvalidWorkspace(de.DomoError):
    def __init__(self, message, domo_instance):
        super().__init__(message, domo_instance)

# %% ../../nbs/classes/50_DomoJupyter.ipynb 23
@patch_to(DomoJupyterWorkspace, cls_method=True)
async def get_current_workspace(
    cls: DomoJupyterWorkspace,
    auth: dmda.DomoAuth,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    try:
        workspace_id = os.environ["DOMO_WORKSPACE_ID"]

    except KeyError as e:
        raise DomoJupyter_InvalidWorkspace(
            message="key error | workspace id not found.  This only works in Domo Jupyter Workspaces",
            domo_instance=auth.domo_instance,
        )

    return await cls.get_by_id(
        workspace_id=workspace_id, auth=auth, debug_api=debug_api, session=session
    )


@patch_to(DomoJupyterWorkspace)
async def get_accounts(
    self: DomoJupyterWorkspace,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
):
    import domolibrary.classes.DomoAccount as dmac

    async def _get_accounts(account_id, auth, props, session, debug_api):
        domo_account = await dmac.DomoAccount.get_by_id(
            account_id=account_id, auth=auth, session=session, debug_api=debug_api
        )
        domo_account.alias = props["alias"]
        return domo_account

    self.domo_accounts_config = await ce.gather_with_concurrency(
        *[
            _get_accounts(
                account_id=account_obj["account_id"],
                auth=self.auth,
                props=account_obj,
                session=session,
                debug_api=debug_api,
            )
            for account_obj in self.account_configuration
        ],
        n=5
    )
    return self.domo_accounts_config

# %% ../../nbs/classes/50_DomoJupyter.ipynb 24
@patch_to(DomoJupyterWorkspace)
async def download_workspace_content(
    self: DomoJupyterWorkspace, base_export_folder=None
) -> str:
    """retrieves content from Domo Jupyter Workspace and downloads to a local folder"""

    base_export_folder = base_export_folder or f"{self.auth.domo_instance}/{self.name}"

    all_content = await self.get_content()
    all_content = [
        content for content in all_content if content.file_type != "directory"
    ]

    return [
        content.export(default_export_folder=base_export_folder)
        for content in all_content
    ]
