# coding:utf-8
import os
import time
import sys
import re
import glob
import serial
from subprocess import Popen, PIPE
from Parameters import *


# Tools functions
def teardown_step(cmd, message=""):
    log.phase_print(f"Teardown : {message}")
    try:
        cmd
    except:
        log.logger.error(message, "Teardown Step KO")
        pass


def run_command(cmd, verbose=False):
    #cmd += ' 2>&1'
    process = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
    output, errors = process.communicate()

    # if process.returncode or errors:
    if process.returncode:
        log.logger.info(f"Return code : {process.returncode}")
        log.logger.info(f"Error : {errors}")
        result = "ERROR"
    else:
        result = str(output)[2:-1]
        result = result.split("\\n")

    if verbose == True:
        log.logger.info(f"--> Run command: {cmd}\n")
        log.logger.info("--> Command returns: ")
        for line in result:
            log.logger.info(line)
    return result


HUB = {"Port_1":  {"location": "2-1",     "port": "3"},
       "Port_3":  {"location": "2-1",     "port": "1"},
       "Port_8":  {"location": "2-1.4.4", "port": "2"},
       "Port_9":  {"location": "2-1.4.4", "port": "1"},
       "Port_10": {"location": "2-1.4.4", "port": "4"}}

def stop_MCU(position):
    #print("Power OFF MCU on HUB port {position}")
    reboot_command=""
    location = HUB[f"Port_{position}"]["location"]
    port = HUB[f"Port_{position}"]["port"]

    reboot_command += f"echo 0 > sudo tee /sys/bus/usb/devices/{location}.{port}/authorized;"        
    reboot_command += f"sudo uhubctl -a off -r 10 -l {location} -p {port};"        
    #reboot_command += f"sudo uhubctl -a off -p {port} -l {location};"
    #reboot_command += f"udevadm trigger --action=remove /sys/bus/usb/devices/{location}.{port}/;"
    # sudo udisksctl power-off --block-device /dev/disk/...
    run_command(reboot_command)


def start_MCU(position):
    #print("Power ON MCU on port {position}")
    start__command=""
    location = HUB[f"Port_{position}"]["location"]
    port = HUB[f"Port_{position}"]["port"]
    start__command += f"sudo uhubctl -a on -p {port} -l {location};"
    start__command += f"echo 1 > sudo tee /sys/bus/usb/devices/{location}.{port}/authorized;"
    run_command(start__command)


def reboot_MCU():  # deprecated : to be deleted
    assert(run_command('./reboot_MCU.sh') != "ERROR")


def available_serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyU[A-Za-z]*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            log.logger.info(port)
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def reinit_serial_port(port):
    try:
        s = serial.Serial(port)
        s.flush()
        s.close()
    except:
        pass


def debug_breakpoint(force_breakpoint=False, message=''):
    if (BREAKPOINT == "ON") or (force_breakpoint == True):
        log.logger.info(f"\n\t*** BREAKPOINT ***  {message}")
        time.sleep(0.1)
        input("\n")


def FATAL(msg="Fatal Error for Debug"):
    log.logger.critical(msg)
    assert("FATAL" == msg)


def device_list():
    return run_command('pio device list --serial --json-output').read()


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


class UsbGate:
    def __init__(self):
        self.usb_gate = 0

    def serial_gate_connection(self, state):
        if state == "OFF":
            log.logger.info("Disconnect Gate USB driver")
            state = "unbind"
            # Search USB Gate number
            usb_nb_cmd = "ls -ll /sys/bus/usb/drivers/ftdi_sio | grep 'devices' | grep 'usb'"
            usb_nb = run_command(usb_nb_cmd)
            assert(usb_nb != -1)
            self.usb_gate = usb_nb[0].split("/")[-1].replace("\n", "")
        elif state == "ON":
            state = "bind"
            log.logger.info("Connect Gate USB driver")
        else:
            raise Exception(
                "Unknown parameter : possible values are \"ON\" or \"OFF\"")

        assert(self.usb_gate != 0)

        # Give writing right access and activate or deactivate serial
        ftdi_driver = "/sys/bus/usb/drivers/ftdi_sio/"
        toggle_usb_cmd = f"echo -n \"{self.usb_gate}\" > {ftdi_driver}"
        run_command(f"chmod 777 {ftdi_driver}{state}; {toggle_usb_cmd}{state}")
        time.sleep(0.1)
