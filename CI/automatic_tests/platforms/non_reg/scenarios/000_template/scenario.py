# coding:utf-8
import os
import sys
import argparse
import time
import serial
from pathlib import Path
from tools.pytest_luos.config.settings import ci_log
from tools.pytest_luos.config.platform import create_platform
from platforms.non_reg.network_config.config import NetworkNodeConfig
from pyluos import Device
from config.parameters import *

# -------------------------------
# Setup and Teardown
# -------------------------------
def setup_nodes(port, upload):
    # Generate node_config.h
    conf= NetworkNodeConfig(__file__, "N5")
    result= conf.nodeConfig_generation()
    time.sleep(0.1)
    assert(result)

    # Create platform
    platform= create_platform()
    platform.init_platform()
    platform.engine.debug_state(DEBUG_MODE)    
    #platform.mcu.start_Node(config_Gate)  #FOR DEBUG

    # Flash code
    if upload == "ON":
        ci_log.phase_log('Flash Gate in G4 ')
        assert(platform.mcu.flash_Node(config_Gate))

    # Setup serial port
    connected_ports = platform.mcu.available_serial_ports()
    ci_log.logger.info(f"Availabled serial ports : {connected_ports}")

    if len(connected_ports) == 0:
        raise Exception("No serial port")
    try:
        for port in connected_ports:
            if platform.luos.port  in port:
                serial_port = port
    except:
        raise Exception("Unknown serial port")
    platform.mcu.reinit_serial_port(port)

    # Connect to platform
    platform.luos.connect(port)
    assert(platform.luos.get_self_connection()) # Stop if connection error
    return platform

def teardown():
    ci_log.phase_log('Start Teardown')
    platform.engine.teardown_step(platform.luos.device.close(), "Closing Device")
    platform.engine.teardown_step(platform.mcu.reinit_serial_port(platform.luos.port), "Closing Serial")


# -------------------------------
# Main
# -------------------------------
if __name__ == '__main__':
    # Arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial_port', type=str, default=gate_Port)
    parser.add_argument('--upload', type=str, default="ON")
    args = parser.parse_args()

    # Setup
    platform = setup_nodes(args.serial_port, args.upload)

    # Run test
    try:
        ci_log.phase_log('Start Template test with G4')
        time.sleep(1)

        services = platform.luos.device.services
        nodes = platform.luos.device.nodes
        ci_log.step_log(services, "Services")
        ci_log.step_log(nodes, "Nodes")

        platform.luos.get_luos_versions("gate")

        ci_log.step_log(f"Start 2 detections", "Step")
        for multiDetection in range(2):
            ci_log.step_log(f"Detection {multiDetection+1}")
            result, retry = platform.luos.ask_detections(delay=1)
            platform.engine.assert_step(result, "Detection OK")
            time.sleep(1)
 
    except Exception as e:
        if 'platform' in locals():
            platform.engine.error_counter = -1
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        ci_log.logger.error(template.format(type(e).__name__, e.args))
        ci_log.logger.error(e)
        pass
    finally:
        if 'platform' in locals():
            teardown()
        else:
            platform.luos.connect()

        sys.exit(platform.engine.test_result())
