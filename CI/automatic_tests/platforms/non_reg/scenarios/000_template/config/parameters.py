# coding:utf-8
from pathlib import Path

# For Debug
DEBUG_MODE = "OFF" # ON to activate breakpoint() method

# Platform parameters
gate_Port = "/dev/ttyUSB"

config_Gate = {"environment": "nucleo_g431kb",
             "flashing_port": {"chipid": "NA", "descriptor": "NA"},
             "path": f"{Path(__file__).parent.resolve()}//../app/N5_NUCLEO_G4",
             "target": "stm32g4x"} 

expected_topology = {'Gate':      ['gate', 'Pipe']}
expected_nodes = ['Gate']
expected_services = ['gate', 'Pipe']
