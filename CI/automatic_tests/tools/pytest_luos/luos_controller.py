# -*- coding: utf-8 -*-
import sys
import io
import serial
import time
import re
from pathlib import Path
from multiprocessing import cpu_count
from pyluos import Device
from tools.pytest_luos.config.settings import *
from tools.pytest_luos.termcolor import colored
from tools.pytest_luos.logger_engine import loggerEngine
from tools.pytest_luos.test_engine import run_command

class LuosControl:
    def __init__(self):
        self.platform= None
        self.connection= False
        self.serial_rate= 1000000
        self.port= 'Unknown'
        self.device= None

    def connect(self, port='Unknown', serial_rate= 1000000):
        self.serial = serial.Serial(baudrate=serial_rate, timeout=0, writeTimeout=0)
        if (port != 'Unknown'):
            ci_log.logger.info(f"Connection to Gate on port {port}")
            try:
                self.device = Device(port)
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
        ci_log.logger.info("\t\t --> Luos Platform Variables")
        for _, item in enumerate(params.items()):
            ci_log.logger.info(f"\t\t\t\t * {item[0]} = {item[1]}")

    def show(self):
        ci_log.logger.info(f"Serial : {self.serial}\nPort : {self.port}\nDevice : {self.device}")


    def check_node_statistics(self, node, required_Node):
        ci_log.logger.info(f"Check statistics for node {node}")        
        keys = ['Ram', 'Rx Msg stack', 'Tx Msg stack', 'Luos stack', 'Buffer occupation',
                'Dropped messages', 'Max Luos loop delay', 'Max Msg retry number']
        values = []
        mesuredStat = {}
        result = ""
        node= node.lower()

        print(f"self.device.{node}.luos_statistics")

        intial_stdout = sys.stdout
        new_stdout = io.StringIO()  # Modify stdout to catch statistics printing
        sys.stdout = new_stdout
        eval(f"self.device.{node}.luos_statistics")
        statistics = new_stdout.getvalue()
        sys.stdout = intial_stdout  # stdout to console
        time.sleep(0.5)        

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
                ci_log.colored_print(f"\t\t\t\t\t\t*RAM :\t\t\t{mesuredStat['Ram']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*RAM :\t\t\t{mesuredStat['Ram']}%", "green")

            if mesuredStat['Tx Msg stack'] > required_Node['Tx Msg stack']:
                result += f"\t{mesuredStat['Tx Msg stack']}% in message stack => Expected value : {required_Node['Tx Msg stack']}%\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Tx Message Stack :\t{mesuredStat['Tx Msg stack']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Tx Message Stack :\t{mesuredStat['Tx Msg stack']}%", "green")

            if mesuredStat['Rx Msg stack'] > required_Node['Rx Msg stack']:
                result += f"\t{mesuredStat['Rx Msg stack']}% in message stack => Expected value : {required_Node['Rx Msg stack']}%\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Rx Message Stack :\t{mesuredStat['Rx Msg stack']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Rx Message Stack :\t{mesuredStat['Rx Msg stack']}%", "green")

            if mesuredStat['Luos stack'] > required_Node['Luos stack']:
                result += f"\t{mesuredStat['Luos stack']}% in Luos stack => Expected value : {required_Node['Luos stack']}%\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Luos Stack :\t\t{mesuredStat['Luos stack']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Luos Stack :\t\t{mesuredStat['Luos stack']}%", "green")

            if mesuredStat['Buffer occupation'] > required_Node['Buffer occupation']:
                result += f"\t{mesuredStat['Buffer occupation']}% of buffer is occupied => Expected value : {required_Node['Buffer occupation']}\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Buffer occupation :\t{mesuredStat['Buffer occupation']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Buffer occupation :\t{mesuredStat['Buffer occupation']}%", "green")

            if mesuredStat['Max Luos loop delay'] > required_Node['Max Luos loop delay']:
                result += f"\t{mesuredStat['Max Luos loop delay']}ms loop delay => Expected value : {required_Node['Max Luos loop delay']}ms\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Max Luos loop delay :\t{mesuredStat['Max Luos loop delay']} ms", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Max Luos loop delay :\t{mesuredStat['Max Luos loop delay']} ms", "green")

            if mesuredStat['Max Msg retry number'] > required_Node['Max Msg retry number']:
                result += f"\t{mesuredStat['Max Msg retry number']} messages retry max => Expected value : {required_Node['Max Msg retry number']}\n"
                ci_log.colored_print(f"\t\t\t\t\t\t\t*Max Msg retry number:  {mesuredStat['Max Msg retry number']}", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Max Msg retry number:  {mesuredStat['Max Msg retry number']}", "green")

            # Assert if there is a dropped message.
            try:
                assert(mesuredStat['Dropped messages'] <= required_Node['Dropped messages'])
            except:
                msg=f"FATAL ERROR : {mesuredStat['Dropped messages']} message(s) dropped !!!!!"
                ci_log.logger.critical(colored(msg, "magenta"))

                time.sleep(1)
                raise Exception(msg)
            if mesuredStat['Dropped messages'] > required_Node['Dropped messages']:
                result += f"\t{mesuredStat['Dropped messages']} messages dropped => Expected value : Max {required_Node['Dropped messages']}\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Dropped messages:\t{mesuredStat['Dropped messages']}", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Dropped messages:\t{mesuredStat['Dropped messages']}", "green")

            if len(result) == 0:
                # ci_log.logger.info(f"\t--> Statistics OK for {service}")
                return "SUCCESS"
            else:
                # eval(f"self.device.{service}.luos_statistics")
                ci_log.logger.critical(colored(f"\t--> Statistics KO for {node}", "magenta"))
                ci_log.logger.critical(colored(result, "magenta"))
                return result
        except:
            error_msg = f"No Statistics received for {node}"
            ci_log.logger.info(error_msg)
            time.sleep(0.1)
            return error_msg

    def check_service_statistics(self, service, requiredStat):
        keys = ['Ram', 'Rx Msg stack', 'Tx Msg stack', 'Luos stack', 'Buffer occupation',
                'Dropped messages', 'Max Luos loop delay', 'Max Msg retry number']
        values = []
        mesuredStat = {}
        result = ""

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
                ci_log.colored_print(f"\t\t\t\t\t\t*RAM :\t\t\t{mesuredStat['Ram']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*RAM :\t\t\t{mesuredStat['Ram']}%", "green")

            if mesuredStat['Tx Msg stack'] > requiredStat['Tx Msg stack']:
                result += f"\t{mesuredStat['Tx Msg stack']}% in message stack => Expected value : {requiredStat['Tx Msg stack']}%\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Tx Message Stack :\t{mesuredStat['Tx Msg stack']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Tx Message Stack :\t{mesuredStat['Tx Msg stack']}%", "green")

            if mesuredStat['Rx Msg stack'] > requiredStat['Rx Msg stack']:
                result += f"\t{mesuredStat['Rx Msg stack']}% in message stack => Expected value : {requiredStat['Rx Msg stack']}%\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Rx Message Stack :\t{mesuredStat['Rx Msg stack']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Rx Message Stack :\t{mesuredStat['Rx Msg stack']}%", "green")

            if mesuredStat['Luos stack'] > requiredStat['Luos stack']:
                result += f"\t{mesuredStat['Luos stack']}% in Luos stack => Expected value : {requiredStat['Luos stack']}%\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Luos Stack :\t\t{mesuredStat['Luos stack']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Luos Stack :\t\t{mesuredStat['Luos stack']}%", "green")

            if mesuredStat['Buffer occupation'] > requiredStat['Buffer occupation']:
                result += f"\t{mesuredStat['Buffer occupation']}% of buffer is occupied => Expected value : {requiredStat['Buffer occupation']}\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Buffer occupation :\t{mesuredStat['Buffer occupation']}%", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Buffer occupation :\t{mesuredStat['Buffer occupation']}%", "green")

            if mesuredStat['Max Luos loop delay'] > requiredStat['Max Luos loop delay']:
                result += f"\t{mesuredStat['Max Luos loop delay']}ms loop delay => Expected value : {requiredStat['Max Luos loop delay']}ms\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Max Luos loop delay :\t{mesuredStat['Max Luos loop delay']} ms", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Max Luos loop delay :\t{mesuredStat['Max Luos loop delay']} ms", "green")

            if mesuredStat['Max Msg retry number'] > requiredStat['Max Msg retry number']:
                result += f"\t{mesuredStat['Max Msg retry number']} messages retry max => Expected value : {requiredStat['Max Msg retry number']}\n"
                ci_log.colored_print(f"\t\t\t\t\t\t\t*Max Msg retry number:  {mesuredStat['Max Msg retry number']}", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Max Msg retry number:  {mesuredStat['Max Msg retry number']}", "green")

            # Assert if there is a dropped message.
            try:
                assert(mesuredStat['Dropped messages'] <=
                       requiredStat['Dropped messages'])
            except:
                msg=f"FATAL ERROR : {mesuredStat['Dropped messages']} message(s) dropped !!!!!"
                ci_log.logger.critical(colored(msg, "magenta"))
                time.sleep(1)
                raise Exception(msg)
            if mesuredStat['Dropped messages'] > requiredStat['Dropped messages']:
                result += f"\t{mesuredStat['Dropped messages']} messages dropped => Expected value : Max {requiredStat['Dropped messages']}\n"
                ci_log.colored_print(f"\t\t\t\t\t\t*Dropped messages:\t{mesuredStat['Dropped messages']}", "red")
            else:
                ci_log.colored_print(f"\t\t\t\t\t\t*Dropped messages:\t{mesuredStat['Dropped messages']}", "green")

            if len(result) == 0:
                # ci_log.logger.info(f"\t--> Statistics OK for {service}")
                return "SUCCESS"
            else:
                # eval(f"self.device.{service}.luos_statistics")
                ci_log.logger.critical(colored(f"\t--> Statistics KO for {service}", "magenta"))
                ci_log.logger.critical(colored(result, "magenta"))
                return result
        except:
            error_msg = f"No Statistics received for {service}"
            ci_log.logger.info(error_msg)
            time.sleep(0.1)
            return error_msg

    def get_luos_versions(self, node):
        node=node.lower()
        for i in range(3):
            try:
                time.sleep(0.5)            
                cmd= eval(f"self.device.{node}.luos_revision")
                break
            except:
                cmd= "No response"
                time.sleep(0.5)
                pass
        ci_log.logger.info(f"[Node {node}]\tLuos revision:  {cmd}")


    def ask_detections(self, delay=0.5):
        time.sleep(delay)
        ci_log.logger.info("Send detection")
        self.device._send({'detection': {}})
        startTime = time.time()
        state = self.device._poll_once()
        retry = 1
        while(1):
            if (retry >= 10):
                return [f"No detection", retry]
            elif (time.time()-startTime > delay):
                retry += 1
                ci_log.logger.info("Send detection")
                self.device._send({'detection': {}})
                startTime = time.time()
            
            state = self.device._poll_once()
            if ('routing_table' in str(state)):
                return ["Detection OK", retry]

    def get_node_number(self, nodes):
        return len(str(nodes).split("node")[1:])


    def build_topology(self, nodes):
        topology = {}
        for node in nodes:
            node = str(node)
            nodeID = node.split("]")[0].split("=")[2].split(",")[0]
            service_in_node = re.findall(r'<(.*?)\>', node)
            service_dict = {}
            for service in service_in_node:
                alias = re.search("\"(.*?)\"", service).group(1)
                id = service.split("=")[-1]
                type = service.split()[0]
                service_dict[alias] = {"id": id, "type": type}
            topology[f"Node_{nodeID}"] = service_dict
        return topology


    def verify_topology(self, nodes, expected_nodes, expected_services):
        # Check all nodes are connected
        topology = self.build_topology(nodes)
        if len(topology.keys()) != len(expected_nodes):
            return False

        # Check all services are connected
        founded_services = 0
        for node in topology.keys():
            for service in topology[node].keys():
                if service in expected_services:
                    founded_services += 1
                    ci_log.logger.info(f"\t- Active service :\t{service}")
                    time.sleep(0.05)
        if founded_services != len(expected_services):
            return False
        return True

    def search_gate(self):
        try:
            gate= run_command("pyluos-discover", verbose=False)
            gate= gate[-2].split('\'')[1]
        except:
            ci_log.logger.warning(f"Pyluos Detection has failed")
            gate= 0
            pass
        return gate