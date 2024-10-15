# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoInstanceConfig.ipynb.

# %% auto 0
__all__ = ['DomoInstanceConfig', 'DomoConnector']

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 2
from ..routes.instance_config_sso import (SSO_AddUserDirectSignonError, SSO_GET_Error, SSO_CRUD_Error)
from ..routes.instance_config import InstanceConfig_Error
from ..routes.publish import GET_Publish_Error

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 3
import httpx
import datetime as dt
from nbdev.showdoc import patch_to
import sys
import pandas as pd

from typing import Any 
from dataclasses import dataclass, field

import domolibrary.utils.DictDot as util_dd
import domolibrary.utils.chunk_execution as ce
import domolibrary.utils.convert as cd

import domolibrary.client.DomoAuth as dmda

import domolibrary.classes.DomoInstanceConfig_UserAttribute as dicua
import domolibrary.classes.DomoInstanceConfig_SSO as dicsso
import domolibrary.classes.DomoInstanceConfig_ApiClient as dicli

import domolibrary.routes.instance_config as instance_config_routes
import domolibrary.routes.sandbox as sandbox_routes
import domolibrary.routes.publish as publish_routes
import domolibrary.routes.application as application_routes

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 6
@dataclass
class DomoInstanceConfig:
    """utility class that absorbs many of the domo instance configuration methods"""

    allowlist: list[str] = field(default_factory=list)

    auth: dmda.DomoAuth = field(repr=False, default=None)
    is_sandbox_self_instance_promotion_enabled: bool = field(default=None)
    is_user_invite_notification_enabled: bool = field(default=None)
    is_invite_social_users_enabled: bool = field(default=None)


    SSO: dicsso.SSO_Config = field(default=None)
    ApiClients: dicli.ApiClients = field(default = None)
    user_attributes: dicua.UserAttributes = field(default = None)
        

    def __post_init__(self):
        self.user_attributes = dicua.UserAttributes(auth=self.auth)
        
        self.SSO = dicsso.SSO(
                auth = self.auth)
        
        self.ApiClients = dicli.ApiClients( auth = self.auth)
        

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 11
@patch_to(DomoInstanceConfig)
async def get_sandbox_is_same_instance_promotion_enabled(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
):
    auth = auth or self.auth

    res = await sandbox_routes.get_is_allow_same_instance_promotion_enabled(
        auth=auth or self.auth,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    self.is_sandbox_self_instance_promotion_enabled = res.response["is_enabled"]

    if return_raw:
        return res

    return res.response

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 14
@patch_to(DomoInstanceConfig)
async def toggle_sandbox_allow_same_instance_promotion(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth,
    is_enabled: bool,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
):
    res = await sandbox_routes.toggle_allow_same_instance_promotion(
        auth=auth or self.auth,
        session=session,
        is_enabled=is_enabled,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    res_is_enabled = await self.get_sandbox_is_same_instance_promotion_enabled()

    if return_raw:
        return res

    return res_is_enabled

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 17
@patch_to(DomoInstanceConfig)
async def get_is_user_invite_notification_enabled(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    """
    Admin > Company Settings > Admin Notifications
    Toggles whether user recieves 'You've been Domo'ed email
    """

    auth = auth or self.auth

    res = await instance_config_routes.get_is_user_invite_notifications_enabled(
        auth=auth or self.auth,
        session=session,
        debug_api=debug_api,
    )

    self.is_user_invite_notification_enabled = res.response["is_enabled"]

    if return_raw:
        return res

    return res.response

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 20
@patch_to(DomoInstanceConfig)
async def toggle_is_user_invite_notification_enabled(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth,
    is_enabled: bool,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    res_is_enabled = await self.get_is_user_invite_notification_enabled(auth=auth)

    if is_enabled == self.is_user_invite_notification_enabled:
        if debug_prn:
            print(
                f"User invite notification is already {'enabled' if is_enabled else 'disabled'} in {auth.domo_instance}"
            )
        return res_is_enabled

    if debug_prn:
        print(
            f"{'enabling' if is_enabled else 'disabling'} User invite notification {auth.domo_instance}"
        )

    res = await instance_config_routes.toggle_is_user_invite_enabled(
        auth=auth or self.auth,
        is_enabled=is_enabled,
        session=session,
        debug_api=debug_api,
    )

    res_is_enabled = await self.get_is_user_invite_notification_enabled(auth=auth)

    if return_raw:
        return res

    return res_is_enabled

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 24
@patch_to(DomoInstanceConfig)
async def get_is_invite_social_users_enabled(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    customer_id: str = None,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    auth = auth or self.auth

    if not customer_id:
        import domolibrary.classes.DomoBootstrap as dmbp

        dmda.test_is_full_auth(auth=auth)

        bs = dmbp.DomoBootstrap(auth=auth)
        customer_id = await bs.get_customer_id()

    res = await instance_config_routes.get_is_invite_social_users_enabled(
        auth=auth or self.auth,
        customer_id=customer_id,
        session=session,
        debug_api=debug_api,
    )

    self.is_invite_social_users_enabled = res.response["is_enabled"]

    if return_raw:
        return res

    return res.response

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 27
@patch_to(DomoInstanceConfig)
async def toggle_is_invite_social_users_enabled(
    self: DomoInstanceConfig,
    is_enabled: bool,
    auth: dmda.DomoFullAuth = None,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    auth = auth or self.auth

    res_is_enabled = await self.get_is_invite_social_users_enabled(auth=auth)

    if is_enabled == self.is_invite_social_users_enabled:
        if debug_prn:
            print(
                f"invite social users is already {'enabled' if is_enabled else 'disabled'} in {auth.domo_instance}"
            )
        return res_is_enabled

    if debug_prn:
        print(
            f"{'enabling' if is_enabled else 'disabling'} invite social users {auth.domo_instance}"
        )

    res = await instance_config_routes.toggle_is_social_users_enabled(
        auth=auth,
        is_enabled=is_enabled,
        session=session,
        debug_api=debug_api,
    )

    res_is_enabled = await self.get_is_invite_social_users_enabled()

    if return_raw:
        return res

    return res_is_enabled

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 31
@patch_to(DomoInstanceConfig)
async def get_is_weekly_digest_enabled(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
    session: httpx.AsyncClient = None,
):

    res = await instance_config_routes.get_is_weekly_digest_enabled(
        auth=auth or self.auth,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    if return_raw:
        return res

    self.is_weekly_digest_enabled = res.response["is_enabled"]

    return res.response

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 33
@patch_to(DomoInstanceConfig)
async def get_is_weekly_digest_enabled(
    self: DomoInstanceConfig,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
    session: httpx.AsyncClient = None,
):

    res = await instance_config_routes.get_is_weekly_digest_enabled(
        auth=self.auth,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    self.is_weekly_digest_enabled = res.response["is_enabled"]

    if return_raw:
        return res

    return res.response

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 35
@patch_to(DomoInstanceConfig)
async def toggle_is_weekly_digest_enabled(
    self: DomoInstanceConfig,
    is_enabled: bool,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_prn: bool = False,
    debug_num_stacks_to_drop=1,
):

    res_is_enabled = await self.get_is_weekly_digest_enabled()

    if is_enabled == self.is_weekly_digest_enabled:
        if debug_prn:
            print(
                f"weekly digest is already {'enabled' if is_enabled else 'disabled'} in {self.auth.domo_instance}"
            )
        return res_is_enabled

    if debug_prn:
        print(
            f"{'enabling' if is_enabled else 'disabling'} weekly digest {self.auth.domo_instance}"
        )

    res = await instance_config_routes.toggle_is_weekly_digest_enabled(
        auth=self.auth,
        is_enabled=is_enabled,
        session=session,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    res_is_enabled = await self.get_is_weekly_digest_enabled()

    if return_raw:
        return res

    return res_is_enabled

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 43
@patch_to(DomoInstanceConfig, cls_method=True)
async def get_publications(
    cls: DomoInstanceConfig,
    auth: dmda.DomoAuth,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    import domolibrary.classes.DomoPublish as dmpb

    res = await publish_routes.search_publications(
        auth=auth, debug_api=debug_api, session=session
    )
    if debug_api:
        print("Getting Publish jobs")

    if res.status == 200 and not return_raw:
        return await ce.gather_with_concurrency(
            n=60,
            *[
                dmpb.DomoPublication.get_from_id(
                    publication_id=job.get("id"), auth=auth
                )
                for job in res.response
            ],
        )

    if res.status == 200 and return_raw:
        return res.response

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 47
@patch_to(DomoInstanceConfig)
async def get_allowlist(
    self: DomoInstanceConfig,
    auth: dmda.DomoFullAuth = None,  # get_allowlist requires full authentication
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_api: bool = False,
) -> list[str]:
    """retrieves the allowlist for an instance"""

    auth = auth or self.auth

    res = None
    loop = 0

    while not res and loop <= 5:
        try:
            res = await instance_config_routes.get_allowlist(
                auth=auth, debug_api=debug_api, session=session
            )
        except Exception as e:
            print(e)
        finally:
            loop += 1

    if return_raw:
        return res

    if not res.is_success:
        return None

    allowlist = res.response.get("addresses")

    self.allowlist = allowlist

    return allowlist

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 51
@patch_to(DomoInstanceConfig)
async def set_allowlist(
    self: DomoInstanceConfig,
    ip_address_ls: list[str],
    debug_api: bool = False,
    auth: dmda.DomoFullAuth = None,
    session: httpx.AsyncClient = None,
):
    auth = auth or self.auth

    await instance_config_routes.set_allowlist(
        auth=auth, ip_address_ls=ip_address_ls, debug_api=debug_api, session=session
    )

    return await self.get_allowlist(auth=auth, debug_api=debug_api, session=session)


@patch_to(
    DomoInstanceConfig,
)
async def upsert_allowlist(
    self: DomoInstanceConfig,
    ip_address_ls: list[str],
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    auth: dmda.DomoAuth = None,
):
    exist_ip_address_ls = await self.get_allowlist(
        auth=auth, debug_api=debug_api, session=session
    )
    ip_address_ls += exist_ip_address_ls

    return await self.set_allowlist(
        auth=auth,
        ip_address_ls=list(set(ip_address_ls)),
        debug_api=debug_api,
        session=session,
    )

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 56
@patch_to(DomoInstanceConfig)
async def get_grants(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth = None,
    debug_prn: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    import domolibrary.classes.DomoGrant as dmg

    auth = auth or self.auth

    return await dmg.DomoGrants.get_grants(
        auth=auth, return_raw=return_raw, session=session, debug_api=debug_api
    )

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 59
@patch_to(DomoInstanceConfig)
async def get_roles(
    self,
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
):
    import domolibrary.classes.DomoRole as dmr

    return await dmr.DomoRoles.get_roles(
        auth=self.auth, debug_api=debug_api, return_raw=return_raw, session=session
    )

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 63
@patch_to(DomoInstanceConfig)
async def get_authorized_domains(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    auth = auth or self.auth

    res = await instance_config_routes.get_authorized_domains(
        auth=auth, debug_api=debug_api, session=session, return_raw=return_raw
    )

    if return_raw:
        return res

    return res.response

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 66
@patch_to(DomoInstanceConfig, cls_method=True)
async def set_authorized_domains(
    cls: DomoInstanceConfig,
    auth: dmda.DomoAuth,
    authorized_domains: list[str],
    debug_prn: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    if debug_prn:
        print(f'🌡️ setting authorized domain with {",".join(authorized_domains)}')

    res = await instance_config_routes.set_authorized_domains(
        auth=auth,
        authorized_domain_ls=authorized_domains,
        debug_api=debug_api,
        session=session,
    )

    if res.status == 200 or res.status == 204:
        dmdic = DomoInstanceConfig(auth=auth)
        res.response = {
            "authorized_domains": await dmdic.get_authorized_domains(
                debug_api=debug_api
            ),
            "status": 200,
        }

    return res


@patch_to(DomoInstanceConfig, cls_method=True)
async def upsert_authorized_domains(
    cls: DomoInstanceConfig,
    auth: dmda.DomoAuth,
    authorized_domains: list[str],
    debug_prn: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    existing_domains = await cls.get_authorized_domains(auth=auth, debug_api=debug_api)

    authorized_domains += existing_domains

    if debug_prn:
        print(f'🌡️ upsertting authorized domain to {",".join(authorized_domains)}')

    return await cls.set_authorized_domains(
        auth=auth,
        authorized_domains=authorized_domains,
        debug_api=debug_api,
        session=session,
    )

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 68
@patch_to(DomoInstanceConfig)
async def get_authorized_custom_app_domains(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    auth = auth or self.auth

    res = await instance_config_routes.get_authorized_custom_app_domains(
        auth=auth, debug_api=debug_api, session=session, return_raw=return_raw
    )

    if return_raw:
        return res

    return res.response

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 72
@patch_to(DomoInstanceConfig, cls_method=True)
async def set_authorized_custom_app_domains(
    cls: DomoInstanceConfig,
    auth: dmda.DomoAuth,
    authorized_domains: list[str],
    debug_prn: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    if debug_prn:
        print(f'🌡️ setting authorized domain with {",".join(authorized_domains)}')

    res = await instance_config_routes.set_authorized_custom_app_domains(
        auth=auth,
        authorized_custom_app_domain_ls=authorized_domains,
        debug_api=debug_api,
        session=session,
    )

    if res.status == 200 or res.status == 204:
        dmdic = DomoInstanceConfig(auth=auth)
        res.response = {
            "authorized_domains": await dmdic.get_authorized_custom_app_domains(
                debug_api=debug_api
            ),
            "status": 200,
        }

    return res


@patch_to(DomoInstanceConfig, cls_method=True)
async def upsert_authorized_custom_app_domains(
    cls: DomoInstanceConfig,
    auth: dmda.DomoAuth,
    authorized_domains: list[str],
    debug_prn: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    existing_domains = await cls.get_authorized_custom_app_domains(
        auth=auth, debug_api=debug_api
    )

    authorized_domains += existing_domains

    if debug_prn:
        print(f'🌡️ upsertting authorized domain to {",".join(authorized_domains)}')

    return await cls.set_authorized_custom_app_domains(
        auth=auth,
        authorized_custom_app_domain_ls=authorized_domains,
        debug_api=debug_api,
        session=session,
    )

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 74
@patch_to(DomoInstanceConfig)
async def get_applications(
    self,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
):
    import domolibrary.classes.DomoApplication as dmapp

    res = await application_routes.get_applications(
        auth=self.auth,
        debug_api=debug_api,
        session=session,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if res.status != 200:
        return res

    return [
        dmapp.DomoApplication._from_json(job, auth=self.auth) for job in res.response
    ]

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 77
@patch_to(DomoInstanceConfig)
async def generate_applications_report(
    self,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
):
    import domolibrary.classes.DomoApplication as dmapp

    domo_apps = await self.get_applications(
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        return_raw=return_raw,
    )

    if return_raw:
        return domo_apps

    df = pd.DataFrame([app.__dict__ for app in domo_apps])
    df["domo_instance"] = self.auth.domo_instance

    df.drop(columns=["auth"], inplace=True)
    df.rename(
        columns={
            "id": "application_id",
            "name": "application_name",
            "description": "application_description",
            "version": "application_version",
        },
        inplace=True,
    )

    return df.sort_index(axis=1)

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 82
@dataclass
class DomoConnector:
    id: str
    label: str
    title: str
    sub_title: str
    description: str
    create_date: dt.datetime
    last_modified: dt.datetime
    publisher_name: str
    writeback_enabled: bool
    tags: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)

    @classmethod
    def _from_str(cls, obj):
        dd = util_dd.DictDot(obj)

        return cls(
            id=dd.databaseId,
            label=dd.label,
            title=dd.title,
            sub_title=dd.subTitle,
            description=dd.description,
            create_date=cd.convert_epoch_millisecond_to_datetime(dd.createDate),
            last_modified=cd.convert_epoch_millisecond_to_datetime(dd.lastModified),
            publisher_name=dd.publisherName,
            writeback_enabled=dd.writebackEnabled,
            tags=dd.tags,
            capabilities=dd.capabilities,
        )

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 83
@patch_to(DomoInstanceConfig)
async def get_connectors(
    self: DomoInstanceConfig,
    auth: dmda.DomoAuth = None,
    search_text=None,
    additional_filters_ls=None,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: httpx.AsyncClient = None,
):
    import domolibrary.routes.datacenter as datacenter_routes

    res = await datacenter_routes.get_connectors(
        auth=auth or self.auth,
        session=session,
        search_text=search_text,
        additional_filters_ls=additional_filters_ls,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    
    if len(res.response) == 0:
        return []


    return [DomoConnector._from_str(obj) for obj in res.response]

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 86
@patch_to(DomoInstanceConfig)
async def get_access_tokens(
    self: DomoInstanceConfig,
    debug_api: bool = False,
    debug_num_stacks_to_drop=3,
    session: httpx.AsyncClient = None,
):
    import domolibrary.classes.DomoAccessToken as dmat

    domo_tokens = await dmat.get_access_tokens(
        auth=self.auth,
        session=session,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    self.access_tokens = domo_tokens

    return self.access_tokens

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 88
@patch_to(DomoInstanceConfig)
async def generate_access_token(
    self: DomoInstanceConfig,
    owner,  # DomoUser
    duration_in_days: int,
    token_name: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=3,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    import domolibrary.classes.DomoAccessToken as dmat

    token = await dmat.DomoAccessToken.generate(
        auth=self.auth,
        session=session,
        token_name=token_name,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        owner=owner,
        duration_in_days=duration_in_days,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        return_raw=return_raw,
    )

    return token

# %% ../../nbs/classes/50_DomoInstanceConfig.ipynb 90
@patch_to(DomoInstanceConfig)
async def regenerate_access_token(
    self,
    domo_user,  # domo_user
    token_name,
    session: httpx.AsyncClient = None,
    duration_in_days: int = 90,
    debug_api: bool = False,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
):

    access_tokens = (
        await self.get_access_tokens(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )
    ) or []

    match_token = next(
        (
            token
            for token in access_tokens
            if token and token.owner == domo_user and token.name == token_name
        ),
        None,
    )

    if match_token:
        await match_token.revoke(
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            debug_api=debug_api,
        )

    domo_access_token = await self.generate_access_token(
        owner=domo_user,
        duration_in_days=duration_in_days,
        token_name=token_name,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        session=session,
        return_raw=return_raw,
    )

    return domo_access_token
