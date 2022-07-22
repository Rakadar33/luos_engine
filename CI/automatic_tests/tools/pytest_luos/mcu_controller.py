# -*- coding: utf-8 -*-
import os
import sys
import glob
import serial
import time
import logging
import logging.config
import subprocess
from multiprocessing import cpu_count
from platformio import fs
from platformio.platform.factory import PlatformFactory
from platformio.project.config import ProjectConfig
from tools.pytest_luos.test_engine import run_command
from tools.pytest_luos.config.settings import *
from tools.pytest_luos.config.settings import ci_log


class McuControl:
    def __init__(self):
        pass

    def available_serial_ports(self):
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/ttyU[A-Za-z]*') # excludes current terminal /dev/tty
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                #ci_log.logger.info(port)
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


    def reinit_serial_port(self, port):
        try:
            s = serial.Serial(port)
            s.flush()
            s.close()
        except:
            pass

    def reboot_MCU(self):  # deprecated : to be deleted
        assert(run_command('./reboot_MCU.sh') != "ERROR")

    def start_Node(self, config):
        if config['target'] == 'dfu':
            return
        pf = PlatformIOApi(config, verbose=False)
        ci_log.logger.info("Restart Node")
        pf.restart()

    def stop_Node(self, config):
        pf = PlatformIOApi(config, verbose=False)
        ci_log.logger.info("Stop Node")
        pf.halt()


    def flash_Node(self, config):
        pf = PlatformIOApi(config, verbose=False)

        ci_log.logger.info("Clean project")
        if (pf.clean(config["environment"]) != 0):
            ci_log.logger.error("********** Cleaning project Error " + config["environment"])
            return False

        '''
        ci_log.logger.info("Compile")
        if (pf.compile(config["environment"]) != 0):
            ci_log.logger.error("********** Compilation Error " + config["environment"])
            return False
        '''

        ci_log.logger.info("Upload program")
        if (pf.upload(config["environment"]) != 0):
            ci_log.logger.error("********** Uploading Error " + config["environment"])
            return False
        # pf.halt()

        # Everything OK
        return True

    def erase_Node(self, config):
        pf = PlatformIOApi(config, verbose=False)

        ci_log.logger.info("Erase program")
        if (pf.erase(config["environment"])):
            return True
        else:
            ci_log.logger.error("********** Erasing Error " + config["environment"])
            return False

class UsbGate:
    def __init__(self):
        self.usb_gate = 0

    def serial_gate_connection(self, state):
        if state == "OFF":
            ci_log.logger.info("Disconnect Gate USB driver")
            state = "unbind"
            # Search USB Gate number
            usb_nb_cmd = "ls -ll /sys/bus/usb/drivers/ftdi_sio | grep 'devices' | grep 'usb'"
            usb_nb = run_command(usb_nb_cmd)
            assert(usb_nb != -1)
            self.usb_gate = usb_nb[0].split("/")[-1].replace("\n", "")
        elif state == "ON":
            state = "bind"
            ci_log.logger.info("Connect Gate USB driver")
        else:
            raise Exception(
                "Unknown parameter : possible values are \"ON\" or \"OFF\"")

        assert(self.usb_gate != 0)

        # Give writing right access and activate or deactivate serial
        ftdi_driver = "/sys/bus/usb/drivers/ftdi_sio/"
        toggle_usb_cmd = f"echo -n \"{self.usb_gate}\" > {ftdi_driver}"
        run_command(f"chmod 777 {ftdi_driver}{state}; {toggle_usb_cmd}{state}")
        time.sleep(0.1)

class PlatformIOApi:
    def __init__(self, configuration, verbose=False):
        self.log = logging.getLogger(self.__class__.__name__)
        self.code_path = configuration["path"]
        #self.flashing_port = configuration["flashing_port"]
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
        ci_log.logger.info(f"Run CLEAN command for {name} environment")
        with fs.cd(self.code_path):
            pio_config = ProjectConfig.get_instance()
            pio_config.validate([name])
            variables = {'pioenv': name, 'project_config': pio_config.path}
            options = pio_config.items(env=name, as_dict=True)
            clean_process = run_command(f'platformio run -t clean -d {self.code_path}')
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
        ci_log.logger.info(f"Run COMPILE command for {name} environment")
        with fs.cd(self.code_path):
            pio_config = ProjectConfig.get_instance()
            pio_config.validate([name])
            variables = {'pioenv': name, 'project_config': pio_config.path}
            options = pio_config.items(env=name, as_dict=True)

            compile_process = run_command(
                f'platformio run -d {self.code_path}', verbose=False)
            if compile_process != "ERROR":
                time.sleep(10)
                return 0
            else:
                return -1
            # ci_log.logger.info(pio_config.envs())
            #platform = PlatformFactory.new(options['platform'])
            # result = platform.run(variables, [], False,
            #                      self.verbose, cpu_count())
            # return result["returncode"]

    def upload(self, name):
        ci_log.logger.info(f"Run UPLOAD command for {name} environment")
        #ci_log.logger.info(self.code_path)
        flash_process = run_command(f'platformio run -t upload -d {self.code_path}', verbose=False, timeout=40)
        if flash_process != "ERROR":
            time.sleep(8)
            return 0
        else:
            ci_log.logger.info(f"ERROR : {name} Flashing command error")
            return -1
        '''
        with fs.cd(self.code_path):
            pio_config = ProjectConfig.get_instance()
            pio_config.validate([name])
            variables = {'pioenv': name, 'project_config': pio_config.path}
            options = pio_config.items(env=name, as_dict=True)
            ci_log.logger.info(pio_config.envs())

            if self.flashing_port == 'DFU':
                # If DFU, add -R option (RESET)to flashing command :
                build_dir = pio_config.path.split("/")[0:-1]
                build_dir = '/'.join([str(item)
                                     for item in build_dir])+'/.pio/build'
                dfuCommand = f"{os.environ['PROJECT_PACKAGES_DIR']}/tool-dfuutil/bin/dfu-util -R -d 0x0483:0xDF11 -a 0 -s 0x08000000:leave -D {build_dir}/{name}/firmware.bin"
                ci_log.logger.info(dfuCommand)
                dfuSuffix = f"{os.environ['PROJECT_PACKAGES_DIR']}/tool-dfuutil/bin/dfu-suffix -v 0x0483 -p 0xDF11 -d 0xffff -a {build_dir}/{name}/firmware.bin"
                ci_log.logger.info(dfuSuffix)
                process = subprocess.run(
                    dfuSuffix, shell=True, check=True, capture_output=True, universal_newlines=True)
                ci_log.logger.info(process.stdout)
                ci_log.logger.info(process.stdout)

                process = subprocess.run(
                    dfuCommand, shell=True, check=True, capture_output=True, universal_newlines=True)
                ci_log.logger.info(process.stdout)
                ci_log.logger.info(process.stdout)
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
                        ci_log.logger.info(
                            f"ERROR 1: {name} Flashing command error")
                        return -1
                else:
                    ci_log.logger.info(
                        f"ERROR 2: {name} environment is not connected")
                    ci_log.critical(
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
                        #ci_log.logger.info(f"USB ID for {label} =\t{os.environ['SERIAL']}")
                        connection = True
                        break

                if connection == True:
                    platform = PlatformFactory.new(options['platform'])
                    result = platform.run(
                        variables, ['upload'], False, self.verbose, cpu_count())
                    return result["returncode"]
                else:
                    ci_log.logger.info(
                        f"ERROR 3: {name} environment is not connected")
                    ci_log.critical(
                        f"ERROR 3: {name} environment is not connected")
                    return -1
        '''

    def erase(self, name):
        if sys.platform != 'linux':
            return -1

        ci_log.logger.info(f"Erase {name} Flash")
        if self._is_board_connected():
            erase_command = stlink_erase.replace(
                "$SERIAL",   self.serial_number)

            # ci_log.logger.info(f"\n\n\nerase_command :  {erase_command}")
            print(erase_command)
            erase_process = run_command(f"{erase_command}", verbose=False)

            if erase_process != "ERROR":
                time.sleep(2)
                return True
            else:
                return False
        else:
            ci_log.logger.info(f"ERROR 4: {name} environment is not connected")
            ci_log.critical(f"ERROR 4: {name} environment is not connected")
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
                    # ci_log.logger.info(str(ST_Info[index-3]))
                    self.serial_number = str(
                        ST_Info[index-3].split(':')[1].replace(' ', '').replace('\n', ''))
                    os.environ['SERIAL'] = self.serial_number
                    #ci_log.logger.info(f"USB ID for {self.flashing_port} =\t{os.environ['SERIAL']}")
                    return True
        return False


    def device_list():
        return run_command('pio device list --serial --json-output').read()
