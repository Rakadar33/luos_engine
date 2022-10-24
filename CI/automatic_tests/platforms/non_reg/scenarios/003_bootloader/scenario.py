# coding:utf-8
import os
import sys
from pyluos import Device
from tools.pytest_luos.config.settings import ci_log
from tools.pytest_luos.test_engine import run_command
from platforms.non_reg.scenario_tools import *
from config.parameters import *
from config.projects import *

def run_scenario(tested_version= "main", upload = "ON"):
    ci_log.phase_log(f'Test Luos Engine \"{tested_version}\" version with config {network_conf}')

    for gate_position in range (network_node_number):
        ci_log.phase_log('Config all projects')

        # Setup the nodes
        gate_node = gate_position + 2 
        product_config_bootloader(gate_node, tested_version)
        platform= setup_nodes(__file__, network_conf, upload)   

        # Verify that the bootloaders are loaded on the nodes
        ci_log.phase_log('Verify that Gate detect all nodes in bootloader mode')
        ci_log.step_log(f"Detection", "Step")
        result, _ = platform.luos.ask_detections(delay=0.5)
        platform.engine.assert_step(result, "Detection OK")

        # Verify Topology
        ci_log.phase_log(f'Verify topology : All nodes should be in bootloader mode')
        services = platform.luos.device.services
        ci_log.step_log(services, "Services")
        nodes = platform.luos.device.nodes
        ci_log.step_log(nodes, "Nodes")
        ci_log.step_log(f"Verify topology", "Step")
        platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_bootloader_topology, expected_bootloader_services), True)

        # Setup Application projects
        platform.luos.device.close()
        product_config_apps(gate_node, tested_version)
        
        ci_log.phase_log("Compile Applications")
        assert(platform.mcu.compile_Node(config_N2))
        assert(platform.mcu.compile_Node(config_N3))
        assert(platform.mcu.compile_Node(config_N4))
        assert(platform.mcu.compile_Node(config_N5))

        # Flash Apps with pyluos-bootloader
        ci_log.phase_log('Flash Apps with pyluos bootloader')
        firmPath = getFirmwarePath(gate_node)

        flash_node_A = f"pyluos-bootloader flash -t {firmPath['node_2']} -b {firmPath['firmware_2']}]"
        flash_node_B = f"pyluos-bootloader flash -t {firmPath['node_3']} -b {firmPath['firmware_3']}]"
        flash_node_C = f"pyluos-bootloader flash -t {firmPath['node_4']} -b {firmPath['firmware_4']}]"
        ci_log.step_log(f"Flash App 1 with bootloader", "Step")
        assert(run_command(flash_node_A, timeout=40, verbose=True) != "ERROR")
        ci_log.step_log(f"Flash App 2 with bootloader", "Step")
        assert(run_command(flash_node_B, timeout=40, verbose=True) != "ERROR")
        ci_log.step_log(f"Flash App 3 with bootloader", "Step")
        assert(run_command(flash_node_C, timeout=40, verbose=True) != "ERROR")

        # Detection
        platform.luos.device.connect()
        ci_log.phase_log('Verify that Gate detects all nodes in App mode')
        ci_log.step_log(f"Detection", "Step")
        result, _ = platform.luos.ask_detections(delay=0.5)
        platform.engine.assert_step(result, "Detection OK")

        # Check Versions
        ci_log.step_log(f"Check Luos engine version", "Step")
        time.sleep(0.1)
        platform.luos.get_luos_versions("Gate")
        time.sleep(0.1)
        platform.luos.get_luos_versions("button")
        time.sleep(0.1)
        platform.luos.get_luos_versions("led")
        time.sleep(0.1)
        platform.luos.get_luos_versions("dc_motor")
        time.sleep(0.1)
        platform.luos.get_luos_versions("potentiometer")
        time.sleep(0.1)

        # Verify topology
        ci_log.phase_log(f'Verify topology: All nodes must be in App mode')
        services = platform.luos.device.services
        ci_log.step_log(services, "Services")
        
        ci_log.step_log(nodes, "Nodes")
        nodes = platform.luos.device.nodes
        
        ci_log.step_log(f"Verify topology", "Step")
        network = platform.luos.verify_topology(nodes, eval(f"expected_topology_N{gate_node}"), eval(f"expected_services_N{gate_node}"))
        platform.engine.assert_step(network, True)

if __name__ == '__main__':
    platform_handler = None
    upload, version = get_arguments()

    try:
        platform_handler = run_scenario(version, upload)
    except Exception as e:
        scenario_exception(e)
        time.sleep(1)
        if "Guru" in str(e) :
            teardown("Guru", platform_handler)
            state= "Fatal"
        else:
            teardown("Exception", platform_handler)
    teardown("OK", platform_handler)    
