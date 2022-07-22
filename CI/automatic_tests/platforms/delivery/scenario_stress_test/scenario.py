# coding:utf-8
import os
import sys
import argparse
import time
import serial
from pathlib import Path
from pyluos import Device
from config.parameters import *
from pytest_luos.config.platform import create_platform

# -------------------------------
# Setup and Teardown
# -------------------------------
def setup_nodes():
    ci_log.phase_log('Setup Nodes')

    '''
    stop_Node(config_G4)
    stop_Node(config_L4)
    stop_Node(config_F0)
    stop_Node(config_Gate)
    time.sleep(0.1)

    ci_log.logger.info('Erasing Nodes...')
    assert(erase_Node(config_G4))
    assert(erase_Node(config_L4))
    #assert(erase_Node(config_Gate))
    '''

    ci_log.logger.info('Flashing Gate...')
    #start_MCU('1')
    time.sleep(5)
    is_gate_flashed = platform.mcu.flash_Node(config_Gate)
    time.sleep(5)
    if not is_gate_flashed:
        #stop_MCU('1')
        assert(is_gate_flashed)

    ci_log.logger.info('Flashing other Nodes...')
    assert(platform.mcu.flash_Node(config_G4))
    assert(platform.mcu.flash_Node(config_L4))
    ci_log.logger.info("Nodes are flashed")    

    '''
    ci_log.logger.info('Stop Gate')
    stop_Node(config_Gate)
    time.sleep(0.5)
    start_Node(config_Gate)
    '''

    time.sleep(0.5)
    '''
    stop_MCU('1')
    start_MCU('1')
    '''    


def setup_port(serial_port):
    connected_ports = platform.mcu.available_serial_ports()
    ci_log.logger.info(f"Availabled serial ports : {connected_ports}")

    if len(connected_ports) == 0:
        raise Exception("No serial port")
    try:
        for port in connected_ports:
            if serial_port in port:
                serial_port = port
    except:
        raise Exception("Unknown serial port")

    # Initialize Serial Port
    platform.mcu.reinit_serial_port(port)
    return serial_port


def teardown():
    ci_log.phase_log('Start Teardown')
    platform.engine.teardown_step(platform.luos.device.close(), "Closing Device")
    platform.engine.teardown_step(platform.mcu.reinit_serial_port(platform.luos.port), "Closing Serial")

# -------------------------------
# Tests definitions
# -------------------------------
def non_regression_test():
    ci_log.phase_log('Start Delivery Platform test')
    time.sleep(1)

    # ----------------------------------------------------------------
    # Step 0 : Function to be put in an external global function
    # ----------------------------------------------------------------
    services = platform.luos.device.services
    time.sleep(1)
    nodes = platform.luos.device.nodes
    ci_log.step_log(services, "Services")
    ci_log.step_log(nodes, "Nodes")
    time.sleep(3)
    platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_topology, expected_services), "Topology OK")

    # Get versions
    for node in node_stat_requirement.keys():    
        try :
            platform.luos.get_luos_versions(node)
        except:
            pass
        time.sleep(0.05)

    # ------------------------
    # Step 1 : Detections
    # ------------------------
    ci_log.step_log("Step 1 :Detection")

    # Several Detections
    ci_log.step_log(f"Start {detection_number} detections", "Step 4")
    for multiDetection in range(detection_number):
        ci_log.step_log(f"Detection {multiDetection+1}")
        result, retry = platform.luos.ask_detections()
        platform.engine.assert_step(result, "Detection OK")
        if result == "Detection OK":
            if retry > 1:
                print(f"{retry} detections sent")
            nodes = platform.luos.device.nodes
            ci_log.step_log(nodes)
            time.sleep(0.2)
            platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_topology, expected_services), "Topology OK")

    # ------------------------
    # Step 2 : State tests
    # ------------------------
    ci_log.step_log("Tests services robustness", "Step 2")

    # Read 15 GPIO states on F4
    ci_log.logger.info("Test F4 Services")
    
    for i in range(15):
        try:
            ci_log.logger.info(f"\t- GPIO {i+1}: ")
            state= eval(f"platform.luos.device.digit_read_{i+1}.state")
            ci_log.logger.info(f"\t\t    * State is {state}")
        except:
            ci_log.logger.info(f"\t\tError : no response from node")
            platform.engine.assert_step("Error in F4 states test", "OK", "ERROR testing F4")
            break


    # Activate Button and LED on G4
    ci_log.logger.info("Test G4 Services")

    try:
        ci_log.logger.info(f"\t-Button state is {platform.luos.device.button_mod.state}")
        ci_log.logger.info("\t-Change RGB Led State")
        platform.luos.device.led_mod.color = [0, 15, 15]
    except:
        ci_log.logger.info(f"\t\tError : no response from node")
        platform.engine.assert_step("Error in G4 states test", "OK", "ERROR testing G4")

    # ---------------------------
    # Step 3 : Statistic control
    # ---------------------------
    ci_log.step_log("Check statistics", "Step 3")
    #'''
    for node in node_stat_requirement.keys():
        time.sleep(0.2)
        platform.engine.assert_step(platform.luos.check_node_statistics(node, node_stat_requirement[node]), "SUCCESS")
    #'''
    #platform.engine.assert_step(platform.luos.check_node_statistics("Gate", node_stat_requirement["Gate"]), "SUCCESS")
    
    # ----------------------------
    # Step 4 : Several Detections
    # ----------------------------
    ci_log.step_log(f"Start {detection_number} detections", "Step 4")
    for multiDetection in range(detection_number):
        ci_log.step_log(f"Detection {multiDetection+1}")
        result, retry = platform.luos.ask_detections()
        platform.engine.assert_step(result, "Detection OK")
        if result == "Detection OK":
            if retry > 1:
                print(f"{retry} detections sent")
            nodes = platform.luos.device.nodes
            ci_log.step_log(nodes)
            time.sleep(0.2)
            platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_topology, expected_services), "Topology OK")

if __name__ == '__main__':
    # Arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('serial', type=str)
    parser.add_argument('upload', type=str)
    args = parser.parse_args()
    
    # Setup
    platform= create_platform()
    platform.init_platform()
    platform.engine.debug_state(DEBUG_MODE)    
    #platform.mcu.start_Node(config_Gate)  #FOR DEBUG

    if args.upload == "ON":
        setup_nodes()
    serial_port = setup_port(args.serial)
    platform.luos.connect(serial_port)

    # Stop test if connection error
    #if not platform.luos.connect():
    if not platform.luos.get_self_connection():
        sys.exit(1)

    # Run test
    try:
        non_regression_test()
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

        # ----------------------
        # Compute test results
        # ----------------------
        result = platform.engine.test_result()
        print(f"LOG file: {ci_log.get_log_filename()}")        
        sys.exit(result)
