# coding:utf-8
from pathlib import Path

# For Debug
DEBUG_MODE = "OFF" # "ON" to enable "breakpoint()"" method

# Platform parameters
expected_topology = {'Gate':  ['gate', 'Pipe'], 'led_1':  ['led_1'], 'led_2':  ['led_2'], 'led_3':  ['led_3'], 'led_4':  ['led_4']}
expected_nodes    = ['Gate', 'led_1', 'led_2', 'led_3', 'led_4']
expected_services = ['gate', 'Pipe', 'led_1', 'led_2', 'led_3', 'led_4']
network_conf = ["N2_N1_N3_N4_N5"]
network_node_number = 5

config_N1 = {"environment": "zero",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/Arduino/button",
             "interruption": "",
             "target": "at91samd"} 
config_N2 = {"environment": "nucleo_f072rb",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/NUCLEO-F072RB/button",
             "interruption": "stm32f0xx_it.c",
             "target": "nucleo_f072rb"} 
config_N3 = {"environment": "nucleo_f401re",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/NUCLEO-F401RE/button",
             "interruption": "stm32f4xx_it.c",
             "target": "nucleo_f401re"} 
config_N4 = {"environment": "nucleo_l432kc",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/NUCLEO-G431KB/button",
             "interruption": "stm32l4xx_it.c",
             "target": "stm32l4x"} 
config_N5 = {"environment": "nucleo_g431kb",
             "path": f"{Path(__file__).parent.resolve()}//../luos_engine/examples/projects/NUCLEO-L432KC/button",
             "interruption": "stm32g4xx_it.c",
             "target": "stm32g4x"} 
