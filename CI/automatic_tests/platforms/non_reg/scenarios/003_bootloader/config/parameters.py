# coding:utf-8
from pathlib import Path

# For Debug
DEBUG_MODE = "OFF" # "ON" to enable "breakpoint()"" method

# Platform parameters
network_conf = ["N2_N3_N4_N5"]
network_node_number = 4

expected_topology = {'Gate':  ['gate', 'Pipe'], 'button':  ['button'], 'dc_motor':  ['dc_motor'], 'potentiometer':  ['potentiometer']}
expected_nodes = list(expected_topology.keys())
expected_services=[]
for services in list(expected_topology.values()):
    for service in services:
        expected_services.append(service)

expected_bootloader_topology = {'Gate':  ['gate', 'Pipe'], 'boot_1':  ['boot_1'], 'boot_2':  ['boot_2'], 'boot_3':  ['boot_3']}
expected_bootloader_nodes = list(expected_bootloader_topology.keys())
expected_bootloader_services=[]
for services in list(expected_bootloader_topology.values()):
    for service in services:
        expected_bootloader_services.append(service)

config_N2 = {"environment": "nucleo_f072rb",
             "path": f"{Path(__file__).parent.resolve()}//../app/N2_NUCLEO_F072/",
             "interruption": "stm32f0xx_it.c",
             "boot_environment": "nucleo_f072rb_with_bootloader",
             "target": "nucleo_f072rb"} 
config_N3 = {"environment": "nucleo_f401re",
             "path": f"{Path(__file__).parent.resolve()}//../app/N3_NUCLEO_F401/",
             "interruption": "stm32f4xx_it.c",
             "boot_environment": "nucleo_f401re_with_bootloader",
             "target": "nucleo_f401re"} 
config_N4 = {"environment": "nucleo_l432kc",
             "path": f"{Path(__file__).parent.resolve()}//../app/N4_NUCLEO_L4/",
             "interruption": "stm32l4xx_it.c",
             "boot_environment": "nucleo_l432kc_with_bootloader",
             "target": "stm32l4x"} 
config_N5 = {"environment": "nucleo_g431kb",
             "path": f"{Path(__file__).parent.resolve()}//../app/N5_NUCLEO_G4/",
             "interruption": "stm32g4xx_it.c",
             "boot_environment": "nucleo_g431kb_with_bootloader",
             "target": "stm32g4x"} 
