# coding:utf-8
from pathlib import Path

# For Debug
DEBUG_MODE = "OFF" # "ON" to enable "breakpoint()"" method

# Platform parameters
expected_topology = {'Gate':  ['gate', 'Pipe', 'led'], 'blinker':  ['blinker']}
expected_nodes    = ['Gate', 'blinker']
expected_services = ['gate', 'Pipe', 'led', 'blinker']



# TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
# TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
# TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!
# TODO : A remettre !!!!!!!!!!!!!!!!!!!!!!!!!    
#network_conf = ["N1_N2", "N2_N5", "N3_N4", "N4_N1", "N5_N3"]


network_conf = ["N2_N5"]

config_N1 = {"environment": "zero",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/Arduino",
             "interruption": "",
             "target": "at91samd"} 
config_N2 = {"environment": "nucleo_f072rb",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-F072RB",
             "interruption": "stm32f0xx_it.c",
             "target": "nucleo_f072rb"} 
config_N3 = {"environment": "nucleo_f401re",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-F401RE",
             "interruption": "stm32f4xx_it.c",
             "target": "nucleo_f401re"} 
config_N4 = {"environment": "nucleo_l432kc",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-L432KC",
             "interruption": "stm32l4xx_it.c",
             "target": "stm32l4x"} 
config_N5 = {"environment": "nucleo_g431kb",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-G431KB",
             "interruption": "stm32g4xx_it.c",
             "target": "stm32g4x"} 
