# coding:utf-8

import os
import sys
import io
import serial
import time
import logging
import logging.config
import subprocess
from multiprocessing import cpu_count
from termcolor import colored
from pathlib import Path
from platformio import fs
from platformio.platform.factory import PlatformFactory
from platformio.project.config import ProjectConfig
from pyluos import Device
from tools import run_command
from Parameters import *


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
        log.logger.info(
            f"Serial : {self.serial}\nPort : {self.port}\nDevice : {self.device}")

    def assert_step(self, obtained, expected, message="", stop_on_failure=False):
        try:
            assert(obtained == expected)
        except:
            log.logger.info(colored("\n[Step KO]", "red"))
            log.logger.critical(
                f"\n[Step KO]\t{message} : \"{obtained}\" instead of \"{expected}\"")
            pass

            if(stop_on_failure):
                time.sleep(0.1)
                raise Exception("[CRITICAL ERROR ON STEP : stop test]")
            else:
                self.error_counter += 1
                pass

    def test_result(self):
        log.phase_print("End of test")
        if(self.error_counter == 0):
            log.logger.info("\n\t--> Test is OK")
            error = 0
        elif (self.error_counter == -1):
            log.logger.warning("\n\t--> Error in test architecture")
            self.assert_step("Error in test architecture", "OK")
            error = -1
        else:
            log.logger.critical(
                f"\n\t--> Test is KO : {self.error_counter} step(s) KO")
            error = -2
        log.logger.info(
            f"\n\nLogs are available in file :\n{log.get_log_filename()}\n\n")
        return error

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


class PlatformIOApi:
    def __init__(self, configuration, verbose=False):
        self.log = logging.getLogger(self.__class__.__name__)
        self.code_path = configuration["path"]
        self.flashing_port = configuration["flashing_port"]
        self.environment = configuration["environment"]
        self.target = configuration["target"]
        self.serial_number = 0
        self.verbose = verbose

    def restart(self):
        assert(self._is_board_connected())
        restart_command = restart_mcu.replace("$TARGET",   self.target)
        restart_process = run_command(restart_command, verbose=False)
        assert(restart_process != "ERROR")

    def halt(self):
        assert(self._is_board_connected())
        halt_command = halt_mcu.replace("$TARGET",   self.target)
        halt_process = run_command(halt_command, verbose=False)
        assert(halt_process != "ERROR")

    def clean(self, name):
        self.log.info(f"Run CLEAN command for {name} environment")
        with fs.cd(self.code_path):
            pio_config = ProjectConfig.get_instance()
            pio_config.validate([name])
            variables = {'pioenv': name, 'project_config': pio_config.path}
            options = pio_config.items(env=name, as_dict=True)
            #clean_process = run_command('/usr/local/bin/platformio run -t clean')
            clean_process = run_command(
                f'cd {self.code_path};platformio run -t clean')
            if clean_process != "ERROR":
                time.sleep(4)
                return 0
            else:
                return -1
            #platform = PlatformFactory.new(options['platform'])
            # result = platform.run(
            #    variables, ['clean'], False, self.verbose, cpu_count())
            # return result["returncode"]

    def compile(self, name):
        self.log.info(f"Run COMPILE command for {name} environment")
        with fs.cd(self.code_path):
            pio_config = ProjectConfig.get_instance()
            pio_config.validate([name])
            variables = {'pioenv': name, 'project_config': pio_config.path}
            options = pio_config.items(env=name, as_dict=True)

            compile_process = run_command(
                f'cd {self.code_path};platformio run', verbose=False)
            if compile_process != "ERROR":
                time.sleep(10)
                return 0
            else:
                return -1
            # log.logger.info(pio_config.envs())
            #platform = PlatformFactory.new(options['platform'])
            # result = platform.run(variables, [], False,
            #                      self.verbose, cpu_count())
            # return result["returncode"]

    def upload(self, name):
        self.log.info(f"Run UPLOAD command for {name} environment")

        # log.logger.info(self.code_path)
        self.log.info(self.code_path)
        flash_process = run_command(
            f'cd {self.code_path};platformio run -t upload', verbose=False)
        if flash_process != "ERROR":
            time.sleep(8)
            return 0
        else:
            log.logger.info(f"ERROR : {name} Flashing command error")
            return -1

        with fs.cd(self.code_path):
            pio_config = ProjectConfig.get_instance()
            pio_config.validate([name])
            variables = {'pioenv': name, 'project_config': pio_config.path}
            options = pio_config.items(env=name, as_dict=True)
            log.logger.info(pio_config.envs())

            if self.flashing_port == 'DFU':
                # If DFU, add -R option (RESET)to flashing command :
                build_dir = pio_config.path.split("/")[0:-1]
                build_dir = '/'.join([str(item)
                                     for item in build_dir])+'/.pio/build'
                dfuCommand = f"{os.environ['PROJECT_PACKAGES_DIR']}/tool-dfuutil/bin/dfu-util -R -d 0x0483:0xDF11 -a 0 -s 0x08000000:leave -D {build_dir}/{name}/firmware.bin"
                log.logger.info(dfuCommand)
                dfuSuffix = f"{os.environ['PROJECT_PACKAGES_DIR']}/tool-dfuutil/bin/dfu-suffix -v 0x0483 -p 0xDF11 -d 0xffff -a {build_dir}/{name}/firmware.bin"
                log.logger.info(dfuSuffix)
                process = subprocess.run(
                    dfuSuffix, shell=True, check=True, capture_output=True, universal_newlines=True)
                log.logger.info(process.stdout)
                self.log.info(process.stdout)

                process = subprocess.run(
                    dfuCommand, shell=True, check=True, capture_output=True, universal_newlines=True)
                log.logger.info(process.stdout)
                self.log.info(process.stdout)
                return 0

            elif isinstance(self.flashing_port, dict):
                if self._is_board_connected():
                    flash_command = stlink_flash.replace(
                        "$SERIAL",   self.serial_number)
                    flash_command = flash_command.replace(
                        "$PROJECT", self.code_path)
                    flash_command = flash_command.replace(
                        "$ENV",     self.environment)

                    flash_process = run_command(flash_command)
                    if flash_process != "ERROR":
                        return 0
                    else:
                        log.logger.info(
                            f"ERROR 1: {name} Flashing command error")
                        return -1
                else:
                    log.logger.info(
                        f"ERROR 2: {name} environment is not connected")
                    self.log.critical(
                        f"ERROR 2: {name} environment is not connected")
                    return -2

            else:
                connectedUSB_process = run_command('ls  /dev/sd*')
                connection = False
                for usb in connectedUSB_process:
                    usb = usb.replace("\n", "")

                    label_process = run_command(
                        f'udevadm info --name={usb} | grep \"ID_FS_LABEL=\"')
                    label = label_process[0].split("=")[-1].replace("\n", "")
                    if label == self.flashing_port.split("/")[-1]:
                        usb_Serial_ID_process = run_command(
                            f'udevadm info --name={usb} | grep ID_SERIAL_SHORT')
                        os.environ['SERIAL'] = usb_Serial_ID_process[0].split("=")[
                            1].replace("\n", "")
                        #log.logger.info(f"USB ID for {label} =\t{os.environ['SERIAL']}")
                        connection = True
                        break

                if connection == True:
                    platform = PlatformFactory.new(options['platform'])
                    result = platform.run(
                        variables, ['upload'], False, self.verbose, cpu_count())
                    return result["returncode"]
                else:
                    log.logger.info(
                        f"ERROR 3: {name} environment is not connected")
                    self.log.critical(
                        f"ERROR 3: {name} environment is not connected")
                    return -1

    def erase(self, name):
        if sys.platform != 'linux':
            return -1

        self.log.info(f"Erase {name} Flash")
        if self._is_board_connected():
            erase_command = stlink_erase.replace(
                "$SERIAL",   self.serial_number)

            # log.logger.info(f"\n\n\nerase_command :  {erase_command}")
            print(erase_command)
            erase_process = run_command(f"{erase_command}", verbose=False)

            if erase_process != "ERROR":
                time.sleep(2)
                return True
            else:
                return False
        else:
            log.logger.info(f"ERROR 4: {name} environment is not connected")
            self.log.critical(f"ERROR 4: {name} environment is not connected")
            return -2

    def _is_board_connected(self):
        '''
        If several STLINKs are connected :
        push SERIAL ID port to environment variable
        '''
        ST_Info = run_command(stlink_detect)
        for index, element in enumerate(ST_Info):
            if self.flashing_port['chipid'] in element:
                descr = ST_Info[index+1]
                if self.flashing_port['descriptor'] in descr:
                    # log.logger.info(str(ST_Info[index-3]))
                    self.serial_number = str(
                        ST_Info[index-3].split(':')[1].replace(' ', '').replace('\n', ''))
                    os.environ['SERIAL'] = self.serial_number
                    #log.logger.info(f"USB ID for {self.flashing_port} =\t{os.environ['SERIAL']}")
                    return True
        return False


def start_Node(config):
    if config['target'] == 'dfu':
        return
    pf = PlatformIOApi(config, verbose=False)
    log.logger.info("Restart Node")
    pf.restart()


def stop_Node(config):
    pf = PlatformIOApi(config, verbose=False)
    log.logger.info("Stop Node")
    pf.halt()


def flash_Node(config, flash=True):
    pf = PlatformIOApi(config, verbose=False)

    if flash == True:
        log.logger.info("Upload program")
        if (pf.upload(config["environment"]) != 0):
            log.logger.error("********** Uploading Error " +
                             config["environment"])
            return False
        # pf.halt()
    else:
        log.logger.info("Clean project")
        if (pf.clean(config["environment"]) != 0):
            log.logger.error(
                "********** Cleaning project Error " + config["environment"])
            return False

        log.logger.info("Compile")
        if (pf.compile(config["environment"]) != 0):
            log.logger.error(
                "********** Compilation Error " + config["environment"])
            return False

    # Everything OK
    return True


def erase_Node(config):
    pf = PlatformIOApi(config, verbose=False)

    log.logger.info("Erase program")
    if (pf.erase(config["environment"])):
        return True
    else:
        log.logger.error("********** Erasing Error " + config["environment"])
        return False
