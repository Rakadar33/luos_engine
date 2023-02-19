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
    for gate_position in range(network_node_number):
        # Setup project
        ci_log.phase_log('Setup project')

        # Select Gate node. The others are buttons
        config_N1["path"].replace("gate_serialcom", "button")
        config_N2["path"].replace("gate_serialcom", "button")
        config_N3["path"].replace("gate_serialcom", "button")
        config_N4["path"].replace("gate_serialcom", "button")
        config_N5["path"].replace("gate_serialcom", "button")
        if gate_position == 0: 
            config_N1["path"].replace("button", "gate_serialcom")
        elif gate_position == 1: 
            config_N2["path"].replace("button", "gate_serialcom")
        elif gate_position == 2: 
            config_N3["path"].replace("button", "gate_serialcom")
        elif gate_position == 3: 
            config_N4["path"].replace("button", "gate_serialcom")
        elif gate_position == 4: 
            config_N5["path"].replace("button", "gate_serialcom")

        ci_log.step_log(f"Clone Luos Engine", "Step")
        if os.path.isdir('luos_engine'):
            try:
                #ci_log.logger.warning(f"Remove luos_engine directory")
                os.remove("luos_engine")
            except:
                error = "Unable to remove luos_engine directory"
                ci_log.logger.critical(error)
                raise ValueError(error)
        cmd = "git clone https://github.com/Luos-io/luos_engine.git"
        run_command(cmd, verbose=True, timeout=20)

        ci_log.step_log(f"Interruptions configuration", "Step")
        source_IT_N2 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N2["interruption"]
        source_IT_N3 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N3["interruption"]
        source_IT_N4 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N4["interruption"]
        source_IT_N5 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N5["interruption"]
        dest_IT_N2 = config_N2["path"] + "src"
        dest_IT_N3 = config_N3["path"] + "src"
        dest_IT_N4 = config_N4["path"] + "src"
        dest_IT_N5 = config_N5["path"] + "src"
        copyfile(source_IT_N2, dest_IT_N2)    
        copyfile(source_IT_N3, dest_IT_N3)    
        copyfile(source_IT_N4, dest_IT_N4)    
        copyfile(source_IT_N5, dest_IT_N5)    

        ci_log.step_log(f"Add Button library to project dependancies", "Step")
        replacetext(eval(f"config_N1[\"path\"]") + "/platformio.ini", "gate_serialcom", f"gate_serialcom\nbutton")
        replacetext(eval(f"config_N2[\"path\"]") + "/platformio.ini", "gate_serialcom", f"gate_serialcom\nbutton")
        replacetext(eval(f"config_N3[\"path\"]") + "/platformio.ini", "gate_serialcom", f"gate_serialcom\nbutton")
        replacetext(eval(f"config_N4[\"path\"]") + "/platformio.ini", "gate_serialcom", f"gate_serialcom\nbutton")
        replacetext(eval(f"config_N5[\"path\"]") + "/platformio.ini", "gate_serialcom", f"gate_serialcom\nbutton")

        # Upload all nodes
        ci_log.phase_log('Flash nodes')
        platform= setup_nodes(__file__, network_conf, upload)

        # Verify multi detections with Gate
        ci_log.phase_log('Verify that \"Gate\" project is working')
        ci_log.step_log(f"Multi detections", "Step")
        for detect in range(100):
            result, _ = platform.luos.ask_detections(delay=0.2)
            platform.engine.assert_step(result, "Detection OK")

        # Check Versions
        ci_log.step_log(f"Check Luos engine version", "Step")
        gate_version = platform.luos.get_luos_versions("gate")
        time.sleep(0.1)
        led1_version = platform.luos.get_luos_versions("button_1")
        time.sleep(0.1)
        led2_version = platform.luos.get_luos_versions("button_2")
        time.sleep(0.1)
        led3_version = platform.luos.get_luos_versions("button_3")
        time.sleep(0.1)
        led4_version = platform.luos.get_luos_versions("button_4")
        time.sleep(0.1)
        #platform.engine.assert_step(gate_version, "2.5.2")
        #platform.engine.assert_step(led1_version, "2.5.2")
        #platform.engine.assert_step(led2_version, "2.5.2")
        #platform.engine.assert_step(led3_version, "2.5.2")
        #platform.engine.assert_step(led4_version, "2.5.2")

        # Verify topology
        ci_log.phase_log(f'Verify topology for {network_conf} configuration')
        services = platform.luos.device.services
        nodes = platform.luos.device.nodes
        ci_log.step_log(services, "Services")
        ci_log.step_log(nodes, "Nodes")
        ci_log.step_log(f"Start detections", "Step")
        platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_topology, expected_services), "Topology OK")
        time.sleep(0.1)

        # TODO : add a configuration with Gate & Pipe on differents nodes
        return platform


if __name__ == '__main__':
    platform, state, upload = get_arguments()
    try:
        platform = run_scenario()
    except Exception as e:
        scenario_exception(e)
        state= "Exception"
    finally:
        teardown(state, platform)
