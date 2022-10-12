# coding:utf-8
from pathlib import Path

# For Debug
DEBUG_MODE = "OFF" # "ON" to enable "breakpoint()"" method

# Platform parameters
network_conf = ["N2_N3_N4_N5"]
network_node_number = 4

expected_bootloader_topology = {
                    'Gate':    ['gate', 'Pipe'],
                    'boot_1':  ['boot_1'],
                    'boot_2':  ['boot_2'],
                    'boot_3':  ['boot_3']}

expected_topology_N2 = {
                    'Gate':           ['gate', 'Pipe'],
                    'led':            ['led'],
                    'dc_motor':       ['dc_motor'],
                    'potentiometer':  ['potentiometer']}

expected_topology_N3 = {
                    'Gate':           ['gate', 'Pipe'],
                    'button':         ['button'],
                    'dc_motor':       ['dc_motor'],
                    'potentiometer':  ['potentiometer']}

expected_topology_N4 = {
                    'Gate':           ['gate', 'Pipe'],
                    'button':         ['button'],
                    'led':            ['led'],
                    'potentiometer':  ['potentiometer']}

expected_topology_N5 = {
                    'Gate':           ['gate', 'Pipe'],
                    'button':         ['button'],
                    'dc_motor':       ['dc_motor'],
                    'led':            ['led']}

expected_bootloader_nodes = list(expected_bootloader_topology.keys())
expected_nodes_N2 = list(expected_topology_N2.keys())
expected_nodes_N3 = list(expected_topology_N3.keys())
expected_nodes_N4 = list(expected_topology_N4.keys())
expected_nodes_N5 = list(expected_topology_N5.keys())

expected_bootloader_services=[]
expected_services_N2=[]
expected_services_N3=[]
expected_services_N4=[]
expected_services_N5=[]

for services in list(expected_bootloader_topology.values()):
    for service in services:
        expected_bootloader_services.append(service)
for services in list(expected_topology_N2.values()):
    for service in services:
        expected_services_N2.append(service)
for services in list(expected_topology_N3.values()):
    for service in services:
        expected_services_N3.append(service)
for services in list(expected_topology_N4.values()):
    for service in services:
        expected_services_N4.append(service)
for services in list(expected_topology_N5.values()):
    for service in services:
        expected_services_N5.append(service)

config_N2 = {"environment": "nucleo_f072rb",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/NUCLEO-F072RB/",
             "app": "button",
             "boot_environment": "nucleo_f072rb_with_bootloader",
             "interruption": "stm32f0xx_it.c",
             "target": "nucleo_f072rb",
             "flashing_port": "N2_F072RB",
             "flashing_options": {"config": "stm32f0x.cfg", "serial": "066AFF544949878667153627"}}

config_N3 = {"environment": "nucleo_f401re",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/NUCLEO-F401RE/",
             "app": "led",
             "boot_environment": "nucleo_f401re_with_bootloader",
             "interruption": "stm32f4xx_it.c",
             "target": "nucleo_f401re",
             "flashing_port": "N3_F401RE",
             "flashing_options": {"config": "stm32f4x.cfg", "serial": "066FFF555054877567045540"}}

config_N4 = {"environment": "nucleo_l432kc",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/NUCLEO-G431KB/",
             "app": "dc_motor",
             "boot_environment": "nucleo_l432kc_with_bootloader",
             "interruption": "stm32l4xx_it.c",
             "target": "stm32l4x",
             "flashing_port": "N4_L432KC",
             "flashing_options": {"config": "stm32l4x.cfg", "serial": "0671FF485688494867102626"}}

config_N5 = {"environment": "nucleo_g431kb",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/NUCLEO-L432KC/",
             "app": "potentiometer",
             "boot_environment": "nucleo_g431kb_with_bootloader",
             "interruption": "stm32g4xx_it.c",
             "target": "stm32g4x",
             "flashing_port": "N5_G431KB",
             "flashing_options": {"config": "stm32g4x.cfg", "serial": "001100174741500720383733"}}
