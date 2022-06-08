# -*- coding: utf-8 -*-
###--import os
import sys
import io
import serial
import time
###--import logging
###--import logging.config
###--import subprocess
from multiprocessing import cpu_count
from termcolor import colored
from pathlib import Path
###--from platformio import fs
###--from platformio.platform.factory import PlatformFactory
###--from platformio.project.config import ProjectConfig
from pyluos import Device
###--from Parameters import *
import pytest_luos.test_engine as TE

class LuosControl:
    def __init__(self):
        pass

class LuosPlatform:
    def __init__(self, port='Unknown', serial_rate=1000000):
        self.connection = False
        self.port = port
        self.serial = serial.Serial(
            baudrate=serial_rate, timeout=0, writeTimeout=0)
        self.error_counter = 0  # should be 0 if test is passed OK
        if (port != 'Unknown'):
            try:
                log.logger.info(f"Start Gate on port {self.port}")
                start_Node(config_Gate)
                self.device = Device(self.port)
                self.connection = True
                time.sleep(0.1)
            except:
                raise EnvironmentError('Luos connection error')
        else:
            raise EnvironmentError('No serial port available')

    def get_self_connection(self):
        return self.connection

    def print_parameters(self):
        params = {}
        params["Serial"] = type(self.serial)
        params["Port"] = self.port
        params["Device"] = self.device
        log.logger.info("\t\t --> Luos Platform Variables")
        for _, item in enumerate(params.items()):
            log.logger.info(f"\t\t\t\t * {item[0]} = {item[1]}")

    def show(self):
        log.logger.info(f"Serial : {self.serial}\nPort : {self.port}\nDevice : {self.device}")


    def check_node_statistics(self, node, required_Node):
        keys = ['Ram', 'Rx Msg stack', 'Tx Msg stack', 'Luos stack', 'Buffer occupation',
                'Dropped messages', 'Max Luos loop delay', 'Max Msg retry number']
        values = []
        mesuredStat = {}
        result = ""

        intial_stdout = sys.stdout
        new_stdout = io.StringIO()  # Modify stdout to catch statistics printing
        sys.stdout = new_stdout
        eval(f"self.device.{expected_topology[node][0]}.luos_statistics")
        statistics = new_stdout.getvalue()
        sys.stdout = intial_stdout  # stdout to console
        get_stats = statistics.split("\n")
        for elt in get_stats:
            elt = elt.split("=")
            try:
                values.append(
                    int(elt[1].replace(" ", "").replace("%", "").replace("ms", "")))
            except:
                pass
        for key, value in zip(keys, values):
            mesuredStat[key] = value

        try:
            if mesuredStat['Ram'] > required_Node['Ram']:
                result += f"\t{mesuredStat['Ram']}% RAM used => Expected value : {required_Node['Ram']}%\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*RAM :\t\t\t{mesuredStat['Ram']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*RAM :\t\t\t{mesuredStat['Ram']}%", "green")

            if mesuredStat['Tx Msg stack'] > required_Node['Tx Msg stack']:
                result += f"\t{mesuredStat['Tx Msg stack']}% in message stack => Expected value : {required_Node['Tx Msg stack']}%\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Tx Message Stack :\t{mesuredStat['Tx Msg stack']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Tx Message Stack :\t{mesuredStat['Tx Msg stack']}%", "green")

            if mesuredStat['Rx Msg stack'] > required_Node['Rx Msg stack']:
                result += f"\t{mesuredStat['Rx Msg stack']}% in message stack => Expected value : {required_Node['Rx Msg stack']}%\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Rx Message Stack :\t{mesuredStat['Rx Msg stack']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Rx Message Stack :\t{mesuredStat['Rx Msg stack']}%", "green")

            if mesuredStat['Luos stack'] > required_Node['Luos stack']:
                result += f"\t{mesuredStat['Luos stack']}% in Luos stack => Expected value : {required_Node['Luos stack']}%\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Luos Stack :\t\t{mesuredStat['Luos stack']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Luos Stack :\t\t{mesuredStat['Luos stack']}%", "green")

            if mesuredStat['Buffer occupation'] > required_Node['Buffer occupation']:
                result += f"\t{mesuredStat['Buffer occupation']}% of buffer is occupied => Expected value : {required_Node['Buffer occupation']}\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Buffer occupation :\t{mesuredStat['Buffer occupation']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Buffer occupation :\t{mesuredStat['Buffer occupation']}%", "green")

            if mesuredStat['Max Luos loop delay'] > required_Node['Max Luos loop delay']:
                result += f"\t{mesuredStat['Max Luos loop delay']}ms loop delay => Expected value : {required_Node['Max Luos loop delay']}ms\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Max Luos loop delay :\t{mesuredStat['Max Luos loop delay']} ms", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Max Luos loop delay :\t{mesuredStat['Max Luos loop delay']} ms", "green")

            if mesuredStat['Max Msg retry number'] > required_Node['Max Msg retry number']:
                result += f"\t{mesuredStat['Max Msg retry number']} messages retry max => Expected value : {required_Node['Max Msg retry number']}\n"
                log.colored_print(
                    f"\t\t\t\t\t\t\t*Max Msg retry number:  {mesuredStat['Max Msg retry number']}", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Max Msg retry number:  {mesuredStat['Max Msg retry number']}", "green")

            # In the future, we should assert if there is at least 1 message dropped.
            # For the moment, just return an error
            '''#Assert if there is a dropped message.
            try:
                assert(mesuredStat['Dropped messages'] <=
                       required_Node['Dropped messages'])
            except:
                msg=f"FATAL ERROR : {mesuredStat['Dropped messages']} message(s) dropped !!!!!"
                log.logger.critical(msg)
                time.sleep(1)
                raise Exception(msg)'''
            if mesuredStat['Dropped messages'] > required_Node['Dropped messages']:
                result += f"\t{mesuredStat['Dropped messages']} messages dropped => Expected value : Max {required_Node['Dropped messages']}\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Dropped messages:\t{mesuredStat['Dropped messages']}", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Dropped messages:\t{mesuredStat['Dropped messages']}", "green")

            if len(result) == 0:
                # log.logger.info(f"\t--> Statistics OK for {service}")
                return "SUCCESS"
            else:
                # eval(f"self.device.{service}.luos_statistics")
                log.logger.critical(f"\t--> Statistics KO for {node}")
                log.logger.critical(result)
                return result
        except:
            error_msg = f"No Statistics received for {node}"
            log.logger.info(error_msg)
            time.sleep(0.1)
            return error_msg

    def check_service_statistics(self, service, requiredStat):
        keys = ['Ram', 'Rx Msg stack', 'Tx Msg stack', 'Luos stack', 'Buffer occupation',
                'Dropped messages', 'Max Luos loop delay', 'Max Msg retry number']
        values = []
        mesuredStat = {}
        result = ""

        eval(f"self.device.{service}.luos_statistics")  # Todo : a enlever

        intial_stdout = sys.stdout
        new_stdout = io.StringIO()  # Modify stdout to catch statistics printing
        sys.stdout = new_stdout
        eval(f"self.device.{service}.luos_statistics")
        statistics = new_stdout.getvalue()
        sys.stdout = intial_stdout  # stdout to console
        get_stats = statistics.split("\n")
        for elt in get_stats:
            elt = elt.split("=")
            try:
                values.append(
                    int(elt[1].replace(" ", "").replace("%", "").replace("ms", "")))
            except:
                pass
        for key, value in zip(keys, values):
            mesuredStat[key] = value

        try:
            if mesuredStat['Ram'] > requiredStat['Ram']:
                result += f"\t{mesuredStat['Ram']}% RAM used => Expected value : {requiredStat['Ram']}%\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*RAM :\t\t\t{mesuredStat['Ram']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*RAM :\t\t\t{mesuredStat['Ram']}%", "green")

            if mesuredStat['Tx Msg stack'] > requiredStat['Tx Msg stack']:
                result += f"\t{mesuredStat['Tx Msg stack']}% in message stack => Expected value : {requiredStat['Tx Msg stack']}%\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Tx Message Stack :\t{mesuredStat['Tx Msg stack']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Tx Message Stack :\t{mesuredStat['Tx Msg stack']}%", "green")

            if mesuredStat['Rx Msg stack'] > requiredStat['Rx Msg stack']:
                result += f"\t{mesuredStat['Rx Msg stack']}% in message stack => Expected value : {requiredStat['Rx Msg stack']}%\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Rx Message Stack :\t{mesuredStat['Rx Msg stack']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Rx Message Stack :\t{mesuredStat['Rx Msg stack']}%", "green")

            if mesuredStat['Luos stack'] > requiredStat['Luos stack']:
                result += f"\t{mesuredStat['Luos stack']}% in Luos stack => Expected value : {requiredStat['Luos stack']}%\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Luos Stack :\t\t{mesuredStat['Luos stack']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Luos Stack :\t\t{mesuredStat['Luos stack']}%", "green")

            if mesuredStat['Buffer occupation'] > requiredStat['Buffer occupation']:
                result += f"\t{mesuredStat['Buffer occupation']}% of buffer is occupied => Expected value : {requiredStat['Buffer occupation']}\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Buffer occupation :\t{mesuredStat['Buffer occupation']}%", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Buffer occupation :\t{mesuredStat['Buffer occupation']}%", "green")

            if mesuredStat['Max Luos loop delay'] > requiredStat['Max Luos loop delay']:
                result += f"\t{mesuredStat['Max Luos loop delay']}ms loop delay => Expected value : {requiredStat['Max Luos loop delay']}ms\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Max Luos loop delay :\t{mesuredStat['Max Luos loop delay']} ms", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Max Luos loop delay :\t{mesuredStat['Max Luos loop delay']} ms", "green")

            if mesuredStat['Max Msg retry number'] > requiredStat['Max Msg retry number']:
                result += f"\t{mesuredStat['Max Msg retry number']} messages retry max => Expected value : {requiredStat['Max Msg retry number']}\n"
                log.colored_print(
                    f"\t\t\t\t\t\t\t*Max Msg retry number:  {mesuredStat['Max Msg retry number']}", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Max Msg retry number:  {mesuredStat['Max Msg retry number']}", "green")

            # In the future, we should assert if there is at least 1 message dropped.
            # For the moment, just return an error
            '''#Assert if there is a dropped message.
            try:
                assert(mesuredStat['Dropped messages'] <=
                       requiredStat['Dropped messages'])
            except:
                msg=f"FATAL ERROR : {mesuredStat['Dropped messages']} message(s) dropped !!!!!"
                log.logger.critical(msg)
                time.sleep(1)
                raise Exception(msg)'''
            if mesuredStat['Dropped messages'] > requiredStat['Dropped messages']:
                result += f"\t{mesuredStat['Dropped messages']} messages dropped => Expected value : Max {requiredStat['Dropped messages']}\n"
                log.colored_print(
                    f"\t\t\t\t\t\t*Dropped messages:\t{mesuredStat['Dropped messages']}", "red")
            else:
                log.colored_print(
                    f"\t\t\t\t\t\t*Dropped messages:\t{mesuredStat['Dropped messages']}", "green")

            if len(result) == 0:
                # log.logger.info(f"\t--> Statistics OK for {service}")
                return "SUCCESS"
            else:
                # eval(f"self.device.{service}.luos_statistics")
                log.logger.critical(f"\t--> Statistics KO for {service}")
                log.logger.critical(result)
                return result
        except:
            error_msg = f"No Statistics received for {service}"
            log.logger.info(error_msg)
            time.sleep(0.1)
            return error_msg

    def get_luos_versions(self):
        # TODO
        pass

    def ask_detections(self, delay=0.2):
        time.sleep(delay)
        log.logger.info("Send detection")
        self.device._send({'detection': {}})
        startTime = time.time()
        state = self.device._poll_once()
        retry = 1
        while(1):
            if (retry >= 10):
                return [f"No detection", retry]
            elif (time.time()-startTime > delay):
                retry += 1
                log.logger.info("Send detection")
                self.device._send({'detection': {}})
                startTime = time.time()
            
            state = self.device._poll_once()
            if ('routing_table' in str(state)):
                return ["Detection OK", retry]

    def get_node_number(nodes):
        return len(str(nodes).split("node")[1:])


    def build_topology(nodes):
        topology = {}
        for node in nodes:
            node = str(node)
            nodeID = str(node).split("]")[0].split("=")[2].split(",")[0]
            service_in_node = re.findall(r'<(.*?)\>', node)
            service_dict = {}
            for service in service_in_node:
                alias = re.search("\"(.*?)\"", service).group(1)
                id = service.split("=")[-1]
                type = service.split()[0]
                service_dict[alias] = {"id": id, "type": type}
            topology[f"Node_{nodeID}"] = service_dict
        return topology


    def verify_topology(platform, nodes):
        topology = build_topology(nodes)
        # Check all nodes are connected
        platform.assert_step(len(topology.keys()),
                             len(expected_nodes), "Check all nodes are connected")

        # Check all services are connected
        founded_services = 0
        for node in topology.keys():
            for service in topology[node].keys():
                if service in expected_services:
                    founded_services += 1
                    log.logger.info(f"\t- Active service :\t{service}")
                    time.sleep(0.05)
        platform.assert_step(founded_services, len(
            expected_services), "Check all services are connected")
