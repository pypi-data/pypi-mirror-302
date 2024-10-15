# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_FactoryAuth.ipynb.

# %% auto 0
__all__ = ['modify_config_generate_config_auth_fn', 'modify_config_generate_admin_auth_fn', 'generate_config_auth',
           'Config_GenerateConfigAuth', 'get_jupyteraccount', 'Config_DomoJupyterToDomoAccount']

# %% ../nbs/00_FactoryAuth.ipynb 1
from .utils.factory import (
    factory_function,
    FactoryLogs, 
    FactoryResponse, FactoryConfig, FactoryMessage)

# %% ../nbs/00_FactoryAuth.ipynb 2
from dataclasses import dataclass
from typing import Callable, Optional

from copy import deepcopy

import domolibrary.client.DomoAuth as dmda
import domolibrary_execution.utils.domojupyter as dxdj

# %% ../nbs/00_FactoryAuth.ipynb 5
async def modify_config_generate_config_auth_fn(step, config,
                                                config_auth_exception : dmda.DomoAuth,
                                                config_auth_standard: dmda.DomoAuth,
                                                target_instance_use_exception_pw : int,
                                                target_instance : str,
                                                **kwargs,
                                                ):
    auth = deepcopy(config_auth_standard)
    step.message = "using standard auth"

    if target_instance_use_exception_pw == 1:
        auth = deepcopy(config_auth_exception)
        step.message = "using exception auth"

    auth.domo_instance = target_instance

    step.is_success = True
    config.auth = auth
    return config

async def modify_config_generate_admin_auth_fn(step, config,
                                                config_auth_prod : dmda.DomoAuth,
                                                config_auth_test: dmda.DomoAuth,
                                                target_instance_use_prod_pw : int,
                                                target_instance: str,
                                                **kwargs,
                                                ):
    auth = deepcopy(config_auth_prod)
    step.message = "using prod auth"

    if target_instance_use_prod_pw == 0:
        auth = deepcopy(config_auth_test)
        step.message = "using test auth"
        step.is_success = True

    auth.domo_instance= target_instance
    step.is_success = True
    config.auth = auth

    return config


@factory_function
async def generate_config_auth(
    config : FactoryConfig,
    res: FactoryResponse,
    modify_config_fn: Optional[Callable] = None,
    # ouptut
    auth : dmda.DomoAuth = None, # will be updated during execution
    debug_api: bool = False,
    
    **kwargs
):

    if modify_config_fn:
        step = FactoryMessage(stage="executing modify_config_fn", stage_num=1)
        step.is_success = False
        res.add_message(step)

        await modify_config_fn(
            **config.asdict(),
            config=config, step=step, debug_api=debug_api
        )

        auth = config.auth    

    res.location = auth.domo_instance

    try:
        step = FactoryMessage(stage="test is valid auth", stage_num = 2)
        res.add_message(step)
        await auth.print_is_token()
        step.is_success = True
        step.message = "valid auth"

    except Exception as e:
        step.message = e
        step.is_success = False

    res.response = auth
    return res


@dataclass
class Config_GenerateConfigAuth(FactoryConfig):
    modify_config_fn : Callable

    # updated during execution
    auth: dmda.DomoAuth = None
    target_instance: str = None



# %% ../nbs/00_FactoryAuth.ipynb 7
@factory_function
async def get_jupyteraccount(
    config: FactoryConfig,
    res : FactoryResponse,
    
    domojupyter_fn : Callable,
    account_name : str, # name of the domo jupyter account and account object to retrieve
    
    account_is_abstract : bool = False,
    modify_config_fn : Callable = None, # can update config


    #updated during execution
    account_creds: dict = None ,

    # used by wrapper
    **kwargs
) -> FactoryResponse:

    step = FactoryMessage(stage="retrieve domojupyter creds")
    res.add_message(step)

    try:
        account_creds = dxdj.read_domo_jupyter_account(
            account_name=account_name,
            domojupyter_fn=domojupyter_fn,
            is_abstract=account_is_abstract,
        )
        step.is_success = True
        step.message = f"domojupyter account {account_name} retrieved"

    except Exception as e:
        step.is_success = False
        step.message = f"failed to retrieve {account_name} - has it been shared with the workbook? {e}"

    if not account_creds:
        res.response = "no creds"
        return res

    config.account_creds = account_creds
    res.response = step.message

    if modify_config_fn:
        step = FactoryMessage(stage=f"modify config", is_success=False)
        res.add_message(step)
        modify_config_fn(config=config, step=step, account_creds=account_creds)

    return res


@dataclass
class Config_DomoJupyterToDomoAccount(FactoryConfig):
    account_name : str # name of the domo jupyter account and account object to retrieve
    domojupyter_fn: Callable
    
    account_is_abstract : bool = False
    
    
    modify_config_fn : Callable = None # can update config

    #updated during execution
    account_creds: dict = None 

