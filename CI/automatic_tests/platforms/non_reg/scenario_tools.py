# coding:utf-8
import sys
import argparse
import time
import re
import serial
from pathlib import Path
from tools.pytest_luos.config.settings import ci_log
from tools.pytest_luos.config.platform import create_platform
from tools.pytest_luos.termcolor import colored
from platforms.non_reg.network_config.config import NetworkNodeConfig
from platforms.non_reg.scenario_tools import *
from pyluos import Device
from config.parameters import *

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', type=str, default="OFF")
    args= parser.parse_args()
    return None, "", args.upload

def setup_nodes(scenario, config, upload="OFF"):
    # Generate node_config.h
    conf= NetworkNodeConfig(scenario, config)
    result= conf.nodeConfig_generation()
    time.sleep(0.1)
    assert(result)

    # Create platform
    platform= create_platform()
    platform.init_platform()
    platform.engine.debug_state(DEBUG_MODE)    
    #platform.mcu.start_Node(config_Gate)  #FOR DEBUG

    if upload == "ON":
        nodes = config.split("_")
        for mcu in nodes:
            ci_log.phase_log(f"[Flash] {mcu}")
            mcu = eval(f"config_{mcu}")
            assert(platform.mcu.flash_Node(mcu))

    # Search for a Gate
    connected_ports = platform.mcu.available_serial_ports()
    ci_log.logger.info(f"Availabled serial ports : {connected_ports}")

    if len(connected_ports) == 0:
        raise Exception("No serial port")

    gate_port = platform.luos.search_gate()
    if gate_port == 0:
        ci_log.logger.critical(colored("No Gate", "magenta"))
        assert(gate_port)
    ci_log.logger.info(f"Gate on port: {gate_port}\n")
    platform.luos.port = gate_port
    platform.mcu.reinit_serial_port(gate_port)

    # Connect to platform
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
    template = "An exception of type \"{0}\" has occurred. Arguments:\n{1!r}"
    error= template.format(type(e).__name__, e.args)
    print(error)
    ci_log.logger.error(error)
    ci_log.logger.error(e)

def teardown(state, platform):
    ci_log.phase_log('Start Teardown')
    if platform != None:
        platform.engine.teardown_step(platform.luos.device.close(), "Closing Device")
        platform.engine.teardown_step(platform.mcu.reinit_serial_port(platform.luos.port), "Closing Serial")
        if (state == "Exception"):
            # Should never occured. If state = Exception, scenario must be modified to handle all exceptions properly.
            platform.engine.error_counter = -1
        sys.exit(platform.engine.test_result())
    else:
        ci_log.logger.critical(colored("[ERROR] Unable to connect to test platform\n\n", "magenta"))
        sys.exit(1)
