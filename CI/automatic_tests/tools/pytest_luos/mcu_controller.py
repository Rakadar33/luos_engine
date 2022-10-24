# -*- coding: utf-8 -*-
import os
import sys
import shutil
import glob
import serial
import time
import logging
import logging.config
import subprocess
from pathlib import Path
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
            ports.extend(glob.glob('/dev/N*'))
            #ports.extend(glob.glob('/dev/ttyACM*'))
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
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
    
    def powerUp_Node(self, nodeNumber):
        #run_command(f"/usr/bin/python3 {os.path.dirname(os.getcwd())}/scripts/capable-robot-driver.py --port {nodeNumber} --power ON")
        run_command(f"export PYTHONPATH=/home/luos_adm/Luos_tests/Docker/Quality_assurance/CI/automatic_tests:$PYTHONPATH;\
                      /usr/bin/python3 \
                      /home/luos_adm/Luos_tests/Docker/Quality_assurance/CI/automatic_tests/tools/scripts/capable-robot-driver.py --port {nodeNumber} --power ON", timeout=5)
    
    def powerDown_Node(self, nodeNumber):    
        #run_command(f"/usr/bin/python3 {os.path.dirname(os.getcwd())}/scripts/capable-robot-driver.py --port {nodeNumber} --power OFF")
        run_command(f"export PYTHONPATH=/home/luos_adm/Luos_tests/Docker/Quality_assurance/CI/automatic_tests:$PYTHONPATH;\
                      /usr/bin/python3 \
                      /home/luos_adm/Luos_tests/Docker/Quality_assurance/CI/automatic_tests/tools/scripts/capable-robot-driver.py --port {nodeNumber} --power OFF", timeout=5)

    def compile_Node(self, config):
        pf = PlatformIOApi(config, verbose=False)

        if (pf.clean(config["environment"]) != 0):
            ci_log.logger.error("********** Cleaning project Error " + config["environment"])
            return False

        if (pf.compile(config["environment"]) != 0):
            ci_log.logger.error("********** Compilation Error " + config["environment"])
            return False

        # Everything OK
        return True

    def flash_Node(self, config):
        pf = PlatformIOApi(config, verbose=False)

        if (pf.clean(config["environment"]) != 0):
            ci_log.logger.error("********** Cleaning project Error " + config["environment"])
            return False

        if (pf.upload(config["environment"]) != 0):
            ci_log.logger.error("********** Uploading Error " + config["environment"])
            return False

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

class UsbControl:
    def __init__(self):
        self.usb_gate= 0
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
            run_command(f"chmod 777 {ftdi_driver}{state}; {toggle_usb_cmd}{state}", timeout=1)

class PlatformIOApi:
    def __init__(self, configuration, verbose=False):
        self.log = logging.getLogger(self.__class__.__name__)
        self.code_path = configuration["path"]
        self.flashing_port = configuration["flashing_port"]
        self.environment = configuration["environment"]
        self.target = configuration["target"]
        self.serial_number = 0
        self.verbose = verbose

    def clean(self, name):
        ci_log.logger.info(f"Clean project {name}")
        clean_process = run_command(f'platformio run -t clean -d {self.code_path}', verbose=False, timeout=5)
        pio_dir= self.code_path + "/.pio/"
        if os.path.isdir(pio_dir):
            try:
                shutil.rmtree(pio_dir)
            except:
                ci_log.logger.critical("Unable to delete .pio directory")
                clean_process = "ERROR"
        if clean_process != "ERROR":
            return 0
        else:
            return -1

    def compile(self, name):
        ci_log.logger.info(f"Compile project {name}")
        with fs.cd(self.code_path):
            pio_config = ProjectConfig.get_instance()
            pio_config.validate([name])
            variables = {'pioenv': name, 'project_config': pio_config.path}
            options = pio_config.items(env=name, as_dict=True)

            compile_process = run_command(f'platformio run -d {self.code_path}', verbose=False, timeout=30)
            if compile_process != "ERROR":
                return 0
            else:
                return -1

    def upload(self, name):
        ci_log.logger.info(f"Upload project {name}")
        flash_process = run_command(f'platformio run -t upload -d {self.code_path}', verbose=False, timeout=40)
        if flash_process != "ERROR":
            return 0
        else:
            ci_log.logger.info(f"ERROR : {name} Flashing command error")
            return -1

    #TODO : TO BE UPDATED
    def erase(self, name):
        if sys.platform != 'linux':
            return -1

        ci_log.logger.info(f"Erase {name} Flash")
        if self._is_board_connected():
            erase_command = stlink_erase.replace(
                "$SERIAL",   self.serial_number)

            # ci_log.logger.info(f"\n\n\nerase_command :  {erase_command}")
            print(erase_command)
            erase_process = run_command(f"{erase_command}", verbose=False, timeout=10)
            if erase_process != "ERROR":
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

def power_down_platform():
    pf= McuControl()
    pf.powerDown_Node(1)
    pf.powerDown_Node(2)
    pf.powerDown_Node(3)
    pf.powerDown_Node(4)
    run_command(f'sudo uhubctl -a off -r 150 -p 3 -l 4-1.4', verbose=False, timeout=30)

