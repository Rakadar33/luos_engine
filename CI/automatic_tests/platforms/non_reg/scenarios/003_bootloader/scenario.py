# coding:utf-8
import os
import sys
from shutil import copyfile
from pyluos import Device
from tools.pytest_luos.config.settings import ci_log
from tools.pytest_luos.config.platform import create_platform
from tools.pytest_luos.test_engine import run_command
from platforms.non_reg.network_config.config import NetworkNodeConfig
from platforms.non_reg.scenario_tools import *
from config.parameters import *

def run_scenario():
    for gate_position in range (network_node_number):
        # Setup project
        ci_log.phase_log('Setup project')

        # Select Bootloader projects for nodes
        ci_log.step_log(f"Flash Gate and other nodes with bootloader", "Step")
        config_N2["path"].replace("N2_NUCLEO_F072", "bootloader")
        config_N3["path"].replace("N3_NUCLEO_F401", "bootloader")
        config_N4["path"].replace("N4_NUCLEO_L4",   "bootloader")
        config_N5["path"].replace("N5_NUCLEO_G4",   "bootloader")
        if gate_position == 0: 
            config_N2["path"].replace("N2_NUCLEO_F072", "gate_serialcom")
        elif gate_position == 1: 
            config_N2["path"].replace("N3_NUCLEO_F401", "gate_serialcom")
        elif gate_position == 2: 
            config_N3["path"].replace("N4_NUCLEO_L4", "gate_serialcom")
        elif gate_position == 3: 
            config_N4["path"].replace("N5_NUCLEO_G4", "gate_serialcom")
        run_command(f"platformio run -d {config_N2["path"]} -t clean")
        run_command(f"platformio run -d {config_N3["path"]} -t clean")
        run_command(f"platformio run -d {config_N4["path"]} -t clean")
        run_command(f"platformio run -d {config_N5["path"]} -t clean")
        run_command(f"platformio run -d {config_N2["path"]} -t upload", timeout= 30)
        run_command(f"platformio run -d {config_N3["path"]} -t upload", timeout= 30)
        run_command(f"platformio run -d {config_N4["path"]} -t upload", timeout= 30)
        run_command(f"platformio run -d {config_N5["path"]} -t upload", timeout= 30)

        # Verify topology
        ci_log.phase_log(f'Verify topology : all nodes are in bootloader mode')
        ci_log.step_log(f"Detection", "Step")
        result, _ = platform.luos.ask_detections(delay=0.5)
        platform.engine.assert_step(result, "Detection OK")

        # Verify topology
        services = platform.luos.device.services
        nodes = platform.luos.device.nodes
        ci_log.step_log(services, "Services")
        ci_log.step_log(nodes, "Nodes")
        ci_log.step_log(f"Verify topology", "Step")
        platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_bootloader_topology, expected_bootloader_services), "Topology OK")
        time.sleep(0.1)

        # ICI ICI ICI ICI ICI ICI ICI  16/07
        ci_log.step_log(f"Bootload App1", "Step")
        ci_log.step_log(f"Detection", "Step")
        ci_log.step_log(f"Bootload App2", "Step")
        ci_log.step_log(f"Detection", "Step")


    # Check Versions
    ci_log.step_log(f"Check Luos engine version", "Step")
    gate_version = platform.luos.get_luos_versions("gate")
    time.sleep(0.1)
    blinker_version = platform.luos.get_luos_versions("blinker")
    time.sleep(0.1)
    #platform.engine.assert_step(gate_version, "2.5.2")
    #platform.engine.assert_step(blinker_version, "2.5.2")




        #--------------------------------

        # Select projects for nodes
        config_N2["path"].replace("gate_serialcom", "button")
        config_N3["path"].replace("gate_serialcom", "dc_motor")
        config_N4["path"].replace("gate_serialcom", "led")
        config_N5["path"].replace("gate_serialcom", "potentiometer")
        if gate_position == 0: 
            config_N2["path"].replace("button", "gate_serialcom")
        elif gate_position == 1: 
            config_N2["path"].replace("dc_motor", "gate_serialcom")
        elif gate_position == 2: 
            config_N3["path"].replace("led", "gate_serialcom")
        elif gate_position == 3: 
            config_N4["path"].replace("potentiometer", "gate_serialcom")


        '''        
        ci_log.step_log(f"Detection", "Step")
        ci_log.step_log(f"Bootload App1", "Step")
        ci_log.step_log(f"Detection", "Step")
        ci_log.step_log(f"Bootload App2", "Step")
        ci_log.step_log(f"Detection", "Step")
        
        -e {config_N1["boot_environment"]}
        -e {config_N2["boot_environment"]}
        -e {config_N3["boot_environment"]}
        -e {config_N4["boot_environment"]}
        

---------------------  
  #Compile projects
    for node in projects:
        try:
            shutil.rmtree(projects[node]+ os.altsep + ".pio")
        except:
            pass
        
        run_command(f"platformio run -d {projects[node]} -t clean")#verbose= True
        run_command(f"platformio run -d {projects[node]}", timeout= 30)
    
    #Bootloader   
    for node in projects:
        #Search firmware
        for root, dir, files in os.walk(projects[node]):
            if "firmware.bin" in files:
                firmware = os.path.join(root, "firmware.bin")
                break

        #Run bootloader   
        run_command(f"pyluos-bootloader flash {serialPort} -t {node} -b {firmware}")
    
    #Verify 
    time.sleep(6)
    run_command(f"pyluos-bootloader detect {serialPort}")
---------------------


        '''    

        ci_log.phase_log('Setup project')

        # Upload all nodes
        ci_log.phase_log('Flash nodes')

        # Verify multi detections with Gate
        ci_log.phase_log('Verify that \"Gate\" project is working')

        # Verify topology
        ci_log.phase_log(f'Verify topology for {network_conf} configuration')


        run_command("pyluos-bootloader detect", verbose=True, timeout=5)
        '''
        run_command("platformio run -t upload -d {path_project}", verbose=True, timeout=20)

        platformio run -t upload -d ./bootloader
        run_command(pyluos-bootloader detect, verbose=True, timeout=5)
        time.sleep(0.5)
        platformio run -t upload -d ./button -e l0_with_bootloader
        run_command(pyluos-bootloader detect, verbose=True, timeout=5)
        time.sleep(0.5)
        platformio run -t upload -d ./led -e l0_with_bootloader
        run_command(pyluos-bootloader detect, verbose=True, timeout=5)
        '''

if __name__ == '__main__':
    platform, state, upload = get_arguments()
    try:
        platform = run_scenario()
    except Exception as e:
        scenario_exception(e)
        state= "Exception"
    finally:
        teardown(state, platform)
