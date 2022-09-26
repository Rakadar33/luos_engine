# coding:utf-8
import os
import sys
from shutil import copyfile, copytree, rmtree
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

    if os.path.isdir('Get_started'):
        try:
            ci_log.logger.warning(f"Remove get started directory")
            for root, dirs, files in os.walk("Get_started", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.removedirs("Get_started")
        except:
            error = "Unable to remove get started directory"
            ci_log.logger.warning(error)
    cmd = "git clone https://github.com/Luos-io/Get_started.git"
    run_command(cmd, verbose=True, timeout=20)

    ci_log.step_log(f"Interruptions configuration", "Step")
    SOURCES = "/src/"
    source_IT_N2 = "../../network_config/" + config_N2["interruption"]
    source_IT_N3 = "../../network_config/" + config_N3["interruption"]
    source_IT_N4 = "../../network_config/" + config_N4["interruption"]
    source_IT_N5 = "../../network_config/" + config_N5["interruption"]
    dest_IT_N2 = config_N2["path"] + SOURCES + config_N2["interruption"]
    dest_IT_N3 = config_N3["path"] + SOURCES + config_N3["interruption"]
    dest_IT_N4 = config_N4["path"] + SOURCES + config_N4["interruption"]
    dest_IT_N5 = config_N5["path"] + SOURCES + config_N5["interruption"]

    copyfile(source_IT_N2, dest_IT_N2)
    copyfile(source_IT_N3, dest_IT_N3)
    copyfile(source_IT_N4, dest_IT_N4)
    copyfile(source_IT_N5, dest_IT_N5)
    
    ci_log.step_log(f"Update Gate project", "Step")
    gate_node= network_conf.split("_")[0]
    node_2= network_conf.split("_")[1]
    gate_sourcecode = eval(f"config_{gate_node}[\"path\"]") + SOURCES + eval(f"config_{gate_node}[\"source\"]")

    # Update platformio.ini Build Flags
    replacetext(eval(f"config_{gate_node}[\"path\"]") + "/platformio.ini",\
                      "node_config.h", f"{gate_node}_node_config.h \n    -I ../../config/")

    ci_log.step_log(f"Update project for second node", "Step")
    led_sourcecode = eval(f"config_{node_2}[\"path\"]") + SOURCES + eval(f"config_{node_2}[\"source\"]")
    replacetext(eval(f"config_{node_2}[\"path\"]") + "/platformio.ini",\
                      "node_config.h", f"{node_2}_node_config.h \n\t-I ../../config/")

    # Update platformio.ini Upload parameters)
    def set_upload_command(config):
        project_config_file= eval(f"config_{config}[\"path\"]") + "/platformio.ini"
        replacetext(project_config_file, "upload_protocol", ";upload_protocol") 
        target_config = eval(f"config_{config}['flashing_options']['config']")
        serial = eval(f"config_{config}['flashing_options']['serial']")
        with open(project_config_file, "a+") as f:
            if config == "N1": #ARDUINO
                flashing_port = 'upload_port = /dev/' + eval(f"config_{config}['flashing_port']")
                replacetext(eval(f"config_{config}[\"path\"]") + "/platformio.ini",\
                                  "\[env\]", f"[env]\n{flashing_port}\n")
            else: #STM32
                f.write('\n')
                f.write('upload_protocol = custom\n')
                f.write('upload_command = openocd -s $PROJECT_PACKAGES_DIR/tool-openocd/scripts -f interface/stlink.cfg -c "transport select hla_swd" $UPLOAD_FLAGS -c "program {$SOURCE} 0x08000000 verify reset; shutdown;"\n')
                f.write('upload_flags =\n')
                f.write('\t-c\n')
                f.write(f'\thla_serial {serial}\n')
                f.write('\t-f\n')
                f.write(f'\ttarget/{target_config}\n')

    set_upload_command(gate_node)
    set_upload_command(node_2)

    tested_version= "fix/pipe_serial"
    luos_engine_version= f"https://github.com/Luos-io/luos_engine.git#{tested_version} ;"
    replacetext(eval(f"config_{gate_node}[\"path\"]") + "/platformio.ini", "luos_engine", luos_engine_version)
    replacetext(eval(f"config_{node_2}[\"path\"]") + "/platformio.ini", "luos_engine", luos_engine_version)
    #assert(1==2)


    # For Arduino : select mkrzero
    # replacetext(eval(f"config_{gate_node}[\"path\"]") + "/platformio.ini", "zero", "mkrzero")

    # Remove "Led" from GATE project
    replacetext(gate_sourcecode, "Led_Init", "//Led_Init")
    replacetext(gate_sourcecode, "Led_Loop", "//Led_Loop")

    # Remove "Gate", "Pipe" and "Blinker" from LED project
    replacetext(led_sourcecode, "Gate_Init", "//Gate_Init")
    replacetext(led_sourcecode, "Pipe_Init", "//Pipe_Init")
    replacetext(led_sourcecode, "Blinker_Init",  "//Blinker_Init")
    replacetext(led_sourcecode, "Gate_Loop", "//Gate_Loop")
    replacetext(led_sourcecode, "Pipe_Loop", "//Pipe_Loop")
    replacetext(led_sourcecode, "Blinker_Loop",  "//Blinker_Loop")

    # Add break boards Power ON in projects
    init_breakboards_gate = "HAL_Platform_Init();"
    init_breakboards_led  = "HAL_Platform_Init();"
    if "Arduino" in gate_sourcecode:
        replace_gate = "Blinker_Init\(\);"
        replace_led  = "\/\* USER CODE END 2 \*\/"
        init_breakboards_gate = "Blinker_Init();" + init_breakboards_gate

    elif "Arduino" in led_sourcecode:
        replace_gate = "\/\* USER CODE END 2 \*\/"
        replace_led  = "Blinker_Init();"
        init_breakboards_led = "Blinker_Init\(\);" + replace_led
    else:
        replace_gate = "\/\* USER CODE END 2 \*\/"
        replace_led  = "\/\* USER CODE END 2 \*\/"
    replacetext(gate_sourcecode, replace_gate, init_breakboards_gate)
    replacetext(led_sourcecode,  replace_led,  init_breakboards_led)

    # Upload all nodes
    ci_log.phase_log('Setup MCUs')
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
    #platform.engine.assert_step(gate_version, expected_version)
    #platform.engine.assert_step(blinker_version, expected_version)

    # Verify topology
    ci_log.phase_log(f'Verify topology for {network_conf} configuration')
    services = platform.luos.device.services
    nodes = platform.luos.device.nodes
    ci_log.step_log(services, "Services")
    ci_log.step_log(nodes, "Nodes")
    ci_log.step_log(f"Start detections", "Step")
    platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_topology, expected_services), True)
    time.sleep(0.1)
    return platform

if __name__ == '__main__':
    platform_handler, state, upload = get_arguments()
    try:
        for conf in network_conf:
            platform_handler = run_scenario(conf)
    except Exception as e:
        scenario_exception(e)
        state= "Exception"
    finally:
        teardown(state, platform_handler)        
