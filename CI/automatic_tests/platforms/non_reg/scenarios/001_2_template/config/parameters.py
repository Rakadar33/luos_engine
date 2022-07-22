# coding:utf-8
from pathlib import Path

# For Debug
DEBUG_MODE = "OFF" # "ON" to enable "breakpoint()"" method

# Platform parameters
network_conf= "N1_N4_N5"
#network_conf= "N2_N1_N3_N4_N5"
gate_Port = "/dev/ttyUSB"

config_N1 = {"environment": "zero",
             "flashing_port": {"chipid": "NA", "descriptor": "NA"},
             "path": f"{Path(__file__).parent.resolve()}//../app/N1_ARDUINO",
             "target": "at91samdXX"} 
config_N2 = {"environment": "nucleo_f072rb",
             "flashing_port": {"chipid": "NA", "descriptor": "NA"},
             "path": f"{Path(__file__).parent.resolve()}//../app/N2_NUCLEO_F072",
             "target": "XXX"} 
config_N3 = {"environment": "nucleo_f401re",
             "flashing_port": {"chipid": "NA", "descriptor": "NA"},
             "path": f"{Path(__file__).parent.resolve()}//../app/N3_NUCLEO_F401",
             "target": "XXX"} 
config_N4 = {"environment": "nucleo_l432kc",
             "flashing_port": {"chipid": "NA", "descriptor": "NA"},
             "path": f"{Path(__file__).parent.resolve()}//../app/N4_NUCLEO_L4",
             "target": "stm32l4x"} 
config_N5 = {"environment": "nucleo_g431kb",
             "flashing_port": {"chipid": "NA", "descriptor": "NA"},
             "path": f"{Path(__file__).parent.resolve()}//../app/N5_NUCLEO_G4",
             "target": "stm32g4x"} 

config_Gate = config_N1 

expected_topology = {'Gate':  ['gate', 'Pipe'], 'Node_5':  ['button']}
expected_nodes    = ['Gate', 'Node_5']
expected_services = ['gate', 'Pipe', 'button']
