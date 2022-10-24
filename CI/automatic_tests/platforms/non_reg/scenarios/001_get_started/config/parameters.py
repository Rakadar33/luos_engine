# coding:utf-8
from pathlib import Path

expected_topology = {'Gate':  ['gate', 'Pipe', 'led'], 'blinker':  ['blinker']}
expected_nodes    = ['Gate', 'blinker']
expected_services = ['gate', 'Pipe', 'led', 'blinker']
network_conf = ["N1_N2", "N2_N5", "N3_N4", "N4_N1", "N5_N3"]
#network_conf = ["N5_N1"]
#network_conf = ["N1_N5"]
network_conf = ["N1_N2"]
#network_conf = ["N4_N1"]
#network_conf = ["N4_N5"]
#network_conf = ["N5_N3"]
#network_conf = ["N5_N2"]
#network_conf = ["N5_N4"]


config_N1 = {"environment": "mkrzero",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/Arduino",
             "interruption": "",
             "source": "Arduino.cpp",
             "target": "at91samd",
             "flashing_port": "N1_Arduino",
             "flashing_options": {"config": "", "serial": ""}}

config_N2 = {"environment": "nucleo_f072rb",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-F072RB",
             "interruption": "stm32f0xx_it.c",
             "source": "main.c",
             "target": "nucleo_f072rb",
             "flashing_port": "N2_F072RB",
             "flashing_options": {"config": "stm32f0x.cfg", "serial": "066AFF544949878667153627"}}

config_N3 = {"environment": "nucleo_f401re",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-F401RE",
             "interruption": "stm32f4xx_it.c",
             "source": "main.c",
             "target": "nucleo_f401re",
             "flashing_port": "N3_F401RE",
             "flashing_options": {"config": "stm32f4x.cfg", "serial": "066FFF555054877567045540"}}

config_N4 = {"environment": "nucleo_l432kc",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-L432KC",
             "interruption": "stm32l4xx_it.c",
             "source": "main.c",
             "target": "stm32l4x",
             "flashing_port": "N4_L432KC",
             "flashing_options": {"config": "stm32l4x.cfg", "serial": "0671FF485688494867102626"}}

config_N5 = {"environment": "nucleo_g431kb",
             "path": f"{Path(__file__).parent.resolve()}//../Get_started/NUCLEO-G431KB",
             "interruption": "stm32g4xx_it.c",
             "source": "main.c",
             "target": "stm32g4x",
             "flashing_port": "N5_G431KB",
             "flashing_options": {"config": "stm32g4x.cfg", "serial": "001100174741500720383733"}}

DEBUG_MODE = "OFF" # For Debug -  "ON" to enable "breakpoint()"" method
