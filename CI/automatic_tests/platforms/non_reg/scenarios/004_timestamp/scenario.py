# coding:utf-8
import os
import sys
from shutil import copyfile
from pyluos import Device
from tools.pytest_luos.config.settings import ci_log
from tools.pytest_luos.config.platform import create_platform
from tools.pytest_luos.test_engine import run_command
from platforms.non_reg.network_config.config import NetworkNodeConfig
from platforms.non_reg.scenario_tools import *
from config.parameters import *

def run_scenario():
    pass
    '''
    - Scenario 4: Timestamp
        - Gate + carte X ⇒ verify 3 differents deltas
        - Launch TU on all boards
        - Conf: matrix
    '''

if __name__ == '__main__':
    platform, state, upload = get_arguments()
    try:
        platform = run_scenario()
    except Exception as e:
        scenario_exception(e)
        state= "Exception"
    finally:
        teardown(state, platform)
