# coding:utf-8
import os
import py_compile
from ssl import SSLSocket
import sys
from pathlib import Path
import argparse
import time
from numpy import quantile
import serial
import json
import logging
from pyluos import Device
'''
from platformio import util
from Parameters import *
from Platform import LuosPlatform, flash_Node, start_Node, stop_Node, erase_Node
from tools import UsbGate, available_serial_ports, reinit_serial_port, teardown_step, verify_topology, build_topology, stop_MCU, start_MCU
'''

sys.path.insert(0, f"{Path(__file__).parents[3]}\\tools")
from pytest_luos.test_engine import LuosPytest
from pytest_luos.logger_engine import log_init, log


# -------------------------------
# Setup and Teardown
# -------------------------------
def setup_nodes(activate_flash_Node="OFF"):
    log.phase_print('Start Setup Nodes')
    '''
    stop_Node(config_G4)
    stop_Node(config_L4)
    stop_Node(config_F0)
    stop_Node(config_Gate)
    time.sleep(0.1)
    '''

    #'''    
    if(activate_flash_Node == "ON"):
        #log.logger.info('Erasing Nodes...')
        assert(erase_Node(config_G4))
        assert(erase_Node(config_L4))
        ##assert(erase_Node(config_F0))
        ##assert(erase_Node(config_Gate))

        log.logger.info('Compiling Nodes...')
        assert(flash_Node(config_G4,    flash=False))
        assert(flash_Node(config_L4,    flash=False))
        ##assert(flash_Node(config_F0,    flash=False))
        assert(flash_Node(config_Gate,  flash=False))

        '''
        log.logger.info('Flashing Gate...')
        start_MCU('1')
        time.sleep(5)
        is_gate_flashed = flash_Node(config_Gate)
        time.sleep(5)
        if not is_gate_flashed:
            stop_MCU('1')
            assert(is_gate_flashed)
        '''

        log.logger.info('Flashing other Nodes...')
        assert(flash_Node(config_G4))
        assert(flash_Node(config_L4))
        ##assert(flash_Node(config_F0))
        log.logger.info("Nodes are flashed")
    #'''

    '''
    log.logger.info('Stop Gate')
    stop_Node(config_Gate)
    time.sleep(0.5)
    start_Node(config_Gate)
    '''
    time.sleep(0.5)
    #stop_MCU('1')
    # start_MCU('1')


def setup_port(serial_port):
    connected_ports = available_serial_ports()
    log.logger.info(f"Availabled serial ports : {connected_ports}")

    if len(connected_ports) == 0:
        raise Exception("No serial port")
    try:
        for port in connected_ports:
            if serial_port in port:
                portCom = port
    except:
        raise Exception("Unknown serial port")

    # Initialize Serial Port
    reinit_serial_port(port)
    return portCom


def teardown(platform_delivery):
    log.phase_print('Start Teardown')
    teardown_step(platform_delivery.device.close(), "Closing Device")
    teardown_step(reinit_serial_port(platform_delivery.port), "Closing Serial")


# -------------------------------
# Tests definitions
# -------------------------------
def non_regression_test(platform):
    log.phase_print('Start Delivery Platform test')
    time.sleep(10)

    # ------------------------
    # Step 1 : Detection
    # ------------------------
    log.step_print("Step 1 :Detection")

    services = platform.device.services
    time.sleep(1)
    nodes = platform.device.nodes
    log.step_print(services, "Services")
    log.step_print(nodes, "Nodes")

    time.sleep(3)
    verify_topology(platform, nodes)

    # Several Detections
    log.step_print(f"Start {detection_number} detections", "Step 4")
    for multiDetection in range(detection_number):
        log.step_print(f"Detection {multiDetection+1}")
        result, retry = platform.ask_detections()
        platform.assert_step(result, "Detection OK")
        if result == "Detection OK":
            if retry > 1:
                print(f"{retry} detections sent")
            nodes = platform.device.nodes
            log.step_print(nodes)
            time.sleep(0.2)
            verify_topology(platform, nodes)



    # ------------------------
    # Step 2 : States tests
    # ------------------------
    log.step_print("Tests services robustness", "Step 2")

    # F0 services
    '''
    log.logger.info("Test F0 Services")

    try:
        log.logger.info(
            f"\t-Button state is {platform.device.button_mod1.state}")
        log.logger.info(
            f"\t-Light intensity is {platform.device.light_sensor_mo.lux}")
        log.logger.info(
            f"\t-Potentiometer position is {platform.device.potentiometer_m.rot_position} degrees")
        log.logger.info("\t-Change RGB Led State")
        platform.device.rgb_led_mod.color = [0, 15, 15]
        log.logger.info(
            f"\t-Servomotor 1 position is {platform.device.servo1_mod.rot_position} degrees")
        log.logger.info(
            f"\t-Servomotor 2 position is {platform.device.servo2_mod.rot_position} degrees")
    except:
        platform.assert_step("Error in F0 states test",
                             "OK", "ERROR testing F0")
    '''

    # Read 15 GPIO states on F4
    log.logger.info("Test F4 Services")

    try:
        log.logger.info(f"\t-GPIO 1 state is {platform.device.digit_read_1.state}")
        log.logger.info(f"\t-GPIO 2 state is {platform.device.digit_read_2.state}")
        log.logger.info(f"\t-GPIO 3 state is {platform.device.digit_read_3.state}")
        log.logger.info(f"\t-GPIO 4 state is {platform.device.digit_read_4.state}")
        log.logger.info(f"\t-GPIO 5 state is {platform.device.digit_read_5.state}")
        log.logger.info(f"\t-GPIO 6 state is {platform.device.digit_read_6.state}")
        log.logger.info(f"\t-GPIO 7 state is {platform.device.digit_read_7.state}")
        log.logger.info(f"\t-GPIO 8 state is {platform.device.digit_read_8.state}")
        log.logger.info(f"\t-GPIO 9 state is {platform.device.digit_read_9.state}")
        log.logger.info(f"\t-GPIO 10 state is {platform.device.digit_read_10.state}")
        log.logger.info(f"\t-GPIO 11 state is {platform.device.digit_read_11.state}")
        log.logger.info(f"\t-GPIO 12 state is {platform.device.digit_read_12.state}")
        log.logger.info(f"\t-GPIO 13 state is {platform.device.digit_read_13.state}")
        log.logger.info(f"\t-GPIO 14 state is {platform.device.digit_read_14.state}")
        log.logger.info(f"\t-GPIO 15 state is {platform.device.digit_read_15.state}")
    except:
        platform.assert_step("Error in F4 states test",
                             "OK", "ERROR testing F4")

    # Activate Button and LED on G4
    log.logger.info("Test G4 Services")

    try:
        log.logger.info(
            f"\t-Button state is {platform.device.button_mod.state}")
        log.logger.info("\t-Change RGB Led State")
        platform.device.led_mod.color = [0, 15, 15]
    except:
        platform.assert_step("Error in G4 states test",
                             "OK", "ERROR testing G4")

    # ---------------------------
    # Step 3 : Statistic control
    # ---------------------------
    log.step_print("Check statistics", "Step 3")

    '''
    # Check stats for each node and service (except Pipe)
    topology = build_topology(nodes)
    for node in topology.keys():
        for service in topology[node].keys():
            if not "Pipe" in service:
                log.logger.info(
                    f"{node} : Check statistic for service {service}")
                time.sleep(0.2)
                platform.assert_step(platform.check_service_statistics(
                    service, service_stat_requirement[service]), "SUCCESS")
    '''
    # Check stats for each node
    topology = build_topology(nodes)
    for node in node_stat_requirement.keys():
        log.logger.info(f"Check statistics for node {node}")
        time.sleep(0.2)
        platform.assert_step(platform.check_node_statistics(
            node, node_stat_requirement[node]), "SUCCESS")
    '''
    for node in topology.keys():
        for service in topology[node].keys():
            log.logger.info(f"{node} : Check statistic for service {service}")
            time.sleep(0.2)
            platform.assert_step(platform.check_service_statistics(
                service, service_stat_requirement[service]), "SUCCESS")
    '''

    # ----------------------------
    # Step 4 : Several Detections
    # ----------------------------
    log.step_print(f"Start {detection_number} detections", "Step 4")
    for multiDetection in range(detection_number):
        log.step_print(f"Detection {multiDetection+1}")
        result, retry = platform.ask_detections()
        platform.assert_step(result, "Detection OK")
        if result == "Detection OK":
            if retry > 1:
                print(f"{retry} detections sent")
            nodes = platform.device.nodes
            log.step_print(nodes)
            time.sleep(0.2)
            verify_topology(platform, nodes)


if __name__ == '__main__':
    # --------------------
    # Arguments parsing
    # --------------------
    '''
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--serial-port', type=str, default=gate_Port)
        parser.add_argument('--upload', type=str, default="ON")
        args = parser.parse_args()
    except:
        print(f"SCENARIO PARAMETERS for scenario {sys.argv[0]}:\n\t\
                --serial-port\t \"Gate serial port number\"\n\t\
                --upload\t \"ON\" or \"OFF\"\n")
        sys.exit()    
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('serial-port', type=str)
    parser.add_argument('upload', type=str, default="ON")
    args = parser.parse_args()


    # --------------------
    # Setup
    # --------------------
    luos_test = LuosPytest()

    log_init()
    setup_nodes(activate_flash_Node=args.upload)
    portCom = setup_port(args.serial_port)
    #HACK (TODO) : add inspector, so fix Gate to ttyUSB0 => to be modified
    #portCom = '/dev/ttyUSB0'
    
    log.logger.info(f"Connection to GATE on port {portCom}")
    platform_delivery = LuosPlatform(portCom)
    # Stop test if connection error
    assert(platform_delivery.get_self_connection())

    # --------------------
    # Run test engine
    # --------------------
    try:
        platform_delivery.get_luos_versions()  # TODO
        non_regression_test(platform_delivery)
    except Exception as e:
        if 'platform_delivery' in locals():
            platform_delivery.error_counter = -1
        log.logger.error(e)
        pass
    finally:
        if 'platform_delivery' in locals():
            teardown(platform_delivery)
        else:
            platform_delivery = LuosPlatform()

        # ----------------------
        # Compute test results
        # ----------------------
        result = platform_delivery.test_result()
        sys.exit(result)
