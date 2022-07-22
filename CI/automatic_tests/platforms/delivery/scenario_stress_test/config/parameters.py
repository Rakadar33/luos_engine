# coding:utf-8
import sys
import copy
from pathlib import Path
sys.path.append(f"{Path(__file__).parents[4]}\\tools")
from pytest_luos.config.settings import *

# For Debug
DEBUG_MODE = "OFF" # ON to activate breakpoint() method

# Platform parameters
gate_Port = "/dev/ttyUSB"

config_F0 = {"environment": "NUCLEO-F042K6",
             "flashing_port": {"chipid": "0x0445", "descriptor": "F04x"},
             "path": f"{Path(__file__).parent.resolve()}//../Projects/NUCLEO_F0",
             "target": "stm32f0x",
             "bootloader": "bootloader_F0.bin"
             }

config_L4 = {"environment": "NUCLEO-L432KC",
             "flashing_port": {"chipid": "0x0435", "descriptor": "L43x/L44x"},
             "path": f"{Path(__file__).parent.resolve()}//../Projects/NUCLEO_L4",
             "target": "stm32l4x",
             "bootloader": "bootloader_L4.bin"
             }
config_G4 = {"environment": "NUCLEO-G431KB",
             "flashing_port": {"chipid": "0x0468", "descriptor": "G4 Category-2"},
             "path": f"{Path(__file__).parent.resolve()}//../Projects/NUCLEO_G4",
             "target": "stm32g4x",
             "bootloader": "bootloader_G4.bin"
             }

config_Gate_STLINK = {"environment": "l0",
             "flashing_port": {"chipid": "0x0448", "descriptor": "F07x"},
             "path": f"{Path(__file__).parent.resolve()}//../../../../Workspace/Luos_engine/examples/projects/l0/gate_serialcom",
             "target": "stm32f0x"
             }

config_Gate_DFU = {"environment": "l0",
             "flashing_port": False,
             "path": f"{Path(__file__).parent.resolve()}//../../../../Workspace/Luos_engine/examples/projects/l0/gate_serialcom",
             "target": "dfu"
             }

config_Gate = config_Gate_STLINK


# Expected values
detection_number = 10

expected_topology = {'Gate':      ['gate', 'Pipe'],
                     'Inspector': ['inspector', 'Pipe1'],
                     'G4':        ['led_mod', 'button_mod'],
                     'L4':        ['digit_read_1', 'digit_read_2', 'digit_read_3', 'digit_read_4', 'digit_read_5', 'digit_read_6', 'digit_read_7', 'digit_read_8',
                                  'digit_read_9', 'digit_read_10', 'digit_read_11', 'digit_read_12', 'digit_read_13', 'digit_read_14', 'digit_read_15']
                     }
expected_nodes = ['Gate', 'L4', 'G4', 'Inspector']
expected_services = ['gate', 'Pipe',
                     'inspector', 'Pipe1',
                     'led_mod', 'button_mod', 
                     'digit_read_1', 'digit_read_2', 'digit_read_3', 'digit_read_4', 'digit_read_5', 'digit_read_6', 'digit_read_7', 'digit_read_8',
                     'digit_read_9', 'digit_read_10', 'digit_read_11', 'digit_read_12', 'digit_read_13', 'digit_read_14', 'digit_read_15']

default_stat = {'Ram': 100,
                'Tx Msg stack': 100,
                'Rx Msg stack': 100,
                'Luos stack': 100,
                'Buffer occupation': 100,
                'Dropped messages': 10,
                'Max Luos loop delay': 10,
                'Max Msg retry number': 10}

service_stat_requirement = {}
for node in expected_topology.keys():
    for service in expected_topology[node]:
        service_stat_requirement[service] = copy.deepcopy(default_stat)


# TODO : fill expected values for all services
# Patch => Gate loop delay has to be fixed in Luos Gate code
service_stat_requirement['gate']['Max Luos loop delay'] = 10

node_stat_requirement = {}
for node in expected_topology.keys():
    node_stat_requirement[node] = copy.deepcopy(default_stat)
# Patch => Gate loop delay has to be fixed in Luos Gate code
node_stat_requirement['Gate']['Max Luos loop delay'] = 10
