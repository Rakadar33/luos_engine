# coding:utf-8
import sys
from pyluos import Device
from tools.pytest_luos.config.settings import ci_log
from tools.pytest_luos.config.platform import create_platform
from platforms.non_reg.network_config.config import NetworkNodeConfig
from platforms.non_reg.scenario_tools import *
from config.parameters import *

def run_scenario(platform):
    ci_log.phase_log('Start Template test with Arduino, L4 and F401')
    time.sleep(0.1)
    services = platform.luos.device.services
    nodes = platform.luos.device.nodes
    ci_log.step_log(services, "Services")
    ci_log.step_log(nodes, "Nodes 5")
    platform.luos.get_luos_versions("gate")
    platform.luos.get_luos_versions("button")
    platform.luos.get_luos_versions("led")
    platform.luos.get_luos_versions("potentiometer")
    platform.luos.get_luos_versions("dc_motor")
    ci_log.step_log(f"Start 2 detections", "Step")
    for multiDetection in range(2):

        ci_log.step_log(f"Detection {multiDetection+1}")
        result, retry = platform.luos.ask_detections(delay=0.5)
        platform.engine.assert_step(result, "Detection OK")
        print(retry)
        time.sleep(0.1)       

if __name__ == '__main__':
    platform, state, upload = get_arguments()
    try:
        platform= setup_nodes(__file__, network_conf, upload)
        run_scenario(platform)
    except Exception as e:
        scenario_exception(e)
        state= "Exception"
    finally:
        teardown(state, platform)
