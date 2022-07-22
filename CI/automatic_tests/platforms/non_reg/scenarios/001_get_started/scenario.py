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

def run_scenario(network_conf):
    # Setup project
    ci_log.phase_log('Setup project')
    ci_log.step_log(f"Clone Get started", "Step")

    # TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
    # TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
    # TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
    # TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!    
    '''
    if os.path.isdir('./Get_started'):
        try:
            #ci_log.logger.warning(f"Remove get started directory")
            os.removedirs("./Get_started") 
        except:
            error = "Unable to remove get started directory"
            ci_log.logger.warning(error)

    cmd = "git clone https://github.com/Luos-io/Get_started.git"

    run_command(cmd, verbose=True, timeout=20)
    '''

    ci_log.step_log(f"Interruptions configuration", "Step")
    SOURCES = "/src"    
    source_IT_N2 = "../../network_config/" + config_N2["interruption"]
    source_IT_N3 = "../../network_config/" + config_N3["interruption"]
    source_IT_N4 = "../../network_config/" + config_N4["interruption"]
    source_IT_N5 = "../../network_config/" + config_N5["interruption"]
    dest_IT_N2 = config_N2["path"] + SOURCES
    dest_IT_N3 = config_N3["path"] + SOURCES
    dest_IT_N4 = config_N4["path"] + SOURCES
    dest_IT_N5 = config_N5["path"] + SOURCES
    copyfile(source_IT_N2, dest_IT_N2)    
    copyfile(source_IT_N3, dest_IT_N3)    
    copyfile(source_IT_N4, dest_IT_N4)    
    copyfile(source_IT_N5, dest_IT_N5)    

    ci_log.step_log(f"Update Gate project", "Step")
    gate_node = network_conf.split("_")[0]    
    gate_sourcecode = eval(f"config_{gate_node}[\"path\"]") + SOURCES
    replacetext(eval(f"config_{gate_node}[\"path\"]") + "/platformio.ini",\
                      "node_config.h", f"{gate_node}_node_config.h \n\t-I ../../config/")
    # Remove "Blinker" from project
    replacetext(gate_sourcecode, "Blinker_Init();", " ")
    replacetext(gate_sourcecode, "Blinker_Loop();", " ")
    
    ci_log.step_log(f"Update Blinker project", "Step")
    blinker_node = network_conf.split("_")[1]
    blinker_sourcecode = eval(f"config_{blinker_node}[\"path\"]") + SOURCES
    replacetext(eval(f"config_{blinker_node}[\"path\"]") + "/platformio.ini",\
                      "node_config.h", f"{blinker_node}_node_config.h \n\t-I ../../config/")
    # Remove "Gate", "Pipe" and "Led" from project
    replacetext(blinker_sourcecode, "Gate_Init();", " ")
    replacetext(blinker_sourcecode, "Pipe_Init();", " ")
    replacetext(blinker_sourcecode, "Led_Init();",  " ")
    replacetext(blinker_sourcecode, "Gate_Loop();", " ")
    replacetext(blinker_sourcecode, "Pipe_Loop();", " ")
    replacetext(blinker_sourcecode, "Led_Loop();",  " ")

    # Upload all nodes
    ci_log.phase_log('Flash nodes')
    platform= setup_nodes(__file__, network_conf, upload)

    # Verify Get started projects
    ci_log.phase_log('Verify that \"Get started\" project is working')
    ci_log.step_log(f"Detection", "Step")
    result, _ = platform.luos.ask_detections(delay=0.5)
    platform.engine.assert_step(result, "Detection OK")

    # Check Versions
    ci_log.step_log(f"Check Luos engine version", "Step")
    gate_version = platform.luos.get_luos_versions("gate")
    time.sleep(0.1)
    blinker_version = platform.luos.get_luos_versions("blinker")
    time.sleep(0.1)
    #platform.engine.assert_step(gate_version, "2.5.2")
    #platform.engine.assert_step(blinker_version, "2.5.2")

    # Verify topology
    ci_log.phase_log(f'Verify topology for {network_conf} configuration')
    services = platform.luos.device.services
    nodes = platform.luos.device.nodes
    ci_log.step_log(services, "Services")
    ci_log.step_log(nodes, "Nodes")
    ci_log.step_log(f"Start detections", "Step")
    platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_topology, expected_services), "Topology OK")
    time.sleep(0.1)
    return platform

if __name__ == '__main__':
    platform, state, upload = get_arguments()
    try:
        for conf in network_conf:
            platform = run_scenario(conf)
    except Exception as e:
        scenario_exception(e)
        state= "Exception"
    finally:
        teardown(state, platform)
