# coding:utf-8
import sys
import argparse
import time
import re
import serial
import traceback
from pathlib import Path
from tools.pytest_luos.config.settings import ci_log
from tools.pytest_luos.config.platform import create_platform
from tools.pytest_luos.mcu_controller import power_down_platform
from tools.pytest_luos.termcolor import colored
from platforms.non_reg.network_config.config import NetworkNodeConfig
from platforms.non_reg.scenario_tools import *
from pyluos import Device
from config.parameters import *

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', type=str, default="OFF")
    parser.add_argument('--version', type=str, default="main")
    args= parser.parse_args()
    return args.upload, args.version

def setup_nodes(scenario, config, upload="OFF"):
    ci_log.phase_log("Setup all nodes")

    # Create platform
    platform= create_platform()
    platform.init_platform()
    platform.engine.debug_state(DEBUG_MODE)    
    try:
        if not isinstance(config, str) :
            config = config[0]
    except:
        pass
    nodes = config.split("_")
    # Generate node_config.h
    conf= NetworkNodeConfig(scenario, config)
    result= conf.nodeConfig_generation()
    assert(result)

    # Power ON nodes
    nodes = config.split("_")
    excluded_nodes= [x for x in range(1,6)]
    for mcu in nodes:
        ci_log.step_log(f"[Power ON] Node {mcu}", "Step")
        number= int(mcu[1])
        if number == 5:
            platform.basic_hub.enable(5)
            excluded_nodes.remove(number)
        elif number < 5:
            platform.mcu.powerUp_Node(number)
            excluded_nodes.remove(number)
        time.sleep(0.1)
    # Power OFF unused nodes 
    for mcu in range(1,6):
        if mcu in excluded_nodes:
            ci_log.step_log(f"[Power OFF] Unused Node {mcu}", "Step")                
            if mcu == 5:
                platform.basic_hub.disable(5)
            else:
                platform.mcu.powerDown_Node(mcu)
            time.sleep(0.1)
    time.sleep(3)

    if upload == "ON":
        # Flash nodes
        ci_log.step_log(f"Flash nodes", "Step")
        for mcu in nodes:
            ci_log.phase_log(f"[Flash] {mcu}")
            mcu = eval(f"config_{mcu}")
            assert(platform.mcu.flash_Node(mcu))
    else:
        # Compile nodes
        ci_log.step_log(f"Compile nodes", "Step")
        for mcu in nodes:
            ci_log.phase_log(f"[Compile] {mcu}")
            mcu = eval(f"config_{mcu}")
            assert(platform.mcu.compile_Node(mcu))

    # Power OFF nodes
    #ci_log.step_log(f"[Power OFF] Nodes", "Step")
    for mcu in nodes:
        number= int(mcu[1])
        if number < 5:
            platform.mcu.powerDown_Node(number)
            time.sleep(0.1)
        elif number == 5:
            platform.basic_hub.disable(number)
    time.sleep(2)

    gate_node = nodes.pop(1) 
    # Power ON all nodes (except Gate)
    for mcu in nodes:
        number = int(mcu[1])
        if number < 5:
            platform.mcu.powerUp_Node(number)
        elif number == 5:
            platform.basic_hub.enable(number)
        time.sleep(1)
    # Power ON the Gate
    number = int(gate_node[1])
    if number < 5:
        platform.mcu.powerUp_Node(number)
    elif number == 5:
        platform.basic_hub.enable(number)
    time.sleep(10)

    # Search for a Gate
    connected_ports = platform.mcu.available_serial_ports()
    ci_log.logger.info(f"Availabled serial ports : {connected_ports}")
    if len(connected_ports) == 0:
        raise Exception("No serial port")

    ci_log.step_log(f"Search a Gate", "Step")
    time.sleep(1)
    gate_max_try = 5
    while gate_max_try:  
        gate_port = platform.luos.search_gate()
        if gate_port != 0:
            break
        else:
            ci_log.logger.info("Retry to find a Gate")   
            time.sleep(1.5)
            gate_max_try -= 1
    if gate_port == 0:
        ci_log.logger.critical(colored("No Gate", "magenta"))
        platform.engine.assert_step("No Gate", "Detection OK", stop_on_failure=True)
    
    ci_log.logger.info(f"Gate on port: {gate_port}\n")
    platform.luos.port = gate_port
    platform.mcu.reinit_serial_port(gate_port)

    # Connect to platform
    ci_log.step_log(f"Connection to Gate - Auto trig detection", "Step")
    platform.luos.connect(gate_port)
    assert(platform.luos.get_self_connection()) # Stop if Gate connection error
    return platform

def replacetext(file, search,replace):
    with open(file,'r+') as f:
        file = f.read()
        file = re.sub(search, replace, file)
        f.seek(0)
        f.write(file)
        f.truncate()

def scenario_exception(e):
    template = f'\n{70*"*"}\n\tWhat ??? An exception occured: {e} \n{70*"*"}'
    error= template.format(type(e).__name__, e.args)
    ci_log.logger.warning(colored(error, "magenta"))
    print(traceback.format_exc())
    ci_log.logger.debug(traceback.format_exc())


    #ci_log.logger.warning(e)

def teardown(state, platform = None):
    ci_log.phase_log('Start Teardown')
    if platform != None:
        try:
            platform.engine.teardown_step("platform.luos.device.close()", "Closing Device")
            time.sleep(0.5)
        except:
            pass
        try:
            platform.engine.teardown_step("platform.mcu.reinit_serial_port(platform.luos.port)", "Closing Serial")
        except:
            pass

        if (state == "Exception"):
            # Should never occured. If state = Exception, scenario must be modified to handle all exceptions properly.
            ci_log.logger.warning("Test scenario EXCEPTION: please modify your scenario to handle this exception")
            platform.engine.error_counter = -1
        elif (state in platform.engine.fatal_exception()):
            platform.engine.error_counter = -2

        result = platform.engine.test_result()

    else:
        ci_log.logger.critical(colored("[ERROR] Unable to connect to test platform\n\n", "magenta"))
        result = -3

    try:
        power_down_platform()
        ci_log.step_log(f"Power Down All Nodes", "Step")
    except:
        ci_log.logger.warning(f"Unable to power down the nodes")
        result = -4
        pass
    sys.exit(result)
