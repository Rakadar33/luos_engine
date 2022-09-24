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

def set_upload_command(config):
    project_config_file= eval(f"config_{config}[\"path\"]") + "/platformio.ini"
    replacetext(project_config_file, "upload_protocol", ";upload_protocol") 
    target_config = eval(f"config_{config}['flashing_options']['config']")
    serial = eval(f"config_{config}['flashing_options']['serial']")
    with open(project_config_file, "a+") as f:
        f.write('\n')
        f.write('upload_protocol = custom\n')
        f.write('upload_command = openocd -s $PROJECT_PACKAGES_DIR/tool-openocd/scripts -f interface/stlink.cfg -c "transport select hla_swd" $UPLOAD_FLAGS -c "program {$SOURCE} 0x08000000 verify reset; shutdown;"\n')
        f.write('upload_flags =\n')
        f.write('\t-c\n')
        f.write(f'\thla_serial {serial}\n')
        f.write('\t-f\n')
        f.write(f'\ttarget/{target_config}\n')

def run_scenario():
    # Project paths
    path_config_N2 = config_N2["path"]
    path_config_N3 = config_N3["path"]
    path_config_N4 = config_N4["path"]
    path_config_N5 = config_N5["path"]

    for gate_position in range (network_node_number):
        gate_node = gate_position + 2 
        # Init project paths
        config_N2["path"] = path_config_N2
        config_N3["path"] = path_config_N2
        config_N4["path"] = path_config_N2
        config_N5["path"] = path_config_N2

        # Setup projects
        # ######################################
        ci_log.phase_log('Setup BOOTLOADER projects')
        # ######################################

        # Clone luos engine
        ci_log.step_log(f"Clone Luos engine", "Step")
        if os.path.isdir('luos_engine'):
            try:
                ci_log.logger.warning(f"Remove luos engine directory")
                for root, dirs, files in os.walk("luos_engine", topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.removedirs("luos_engine")
            except:
                error = "Unable to remove luos engine directory"
                ci_log.logger.warning(error)
        cmd = "git clone https://github.com/Luos-io/luos_engine.git"
        run_command(cmd, verbose=True, timeout=20)

        # Select Gate & Bootloaders projects for nodes
        ci_log.step_log(f"Flash Gate and other nodes with bootloader", "Step")
        if gate_node == 2: 
            config_N2["path"] += "gate_serialcom"
            config_N3["path"] += "bootloader"
            config_N4["path"] += "bootloader"
            config_N5["path"] += "bootloader"
        if gate_node == 3: 
            config_N2["path"] += "bootloader"
            config_N3["path"] += "gate_serialcom"
            config_N4["path"] += "bootloader"
            config_N5["path"] += "bootloader"
        if gate_node == 4: 
            config_N2["path"] += "bootloader"
            config_N3["path"] += "bootloader"
            config_N4["path"] += "gate_serialcom"
            config_N5["path"] += "bootloader"
        if gate_node == 5: 
            config_N2["path"] += "bootloader"
            config_N3["path"] += "bootloader"
            config_N4["path"] += "bootloader"
            config_N5["path"] += "gate_serialcom"

        ci_log.step_log(f"Interruptions configuration", "Step")
        SOURCES = "/src/"
        source_IT_N2 = "../../network_config/" + config_N2["interruption"]
        source_IT_N3 = "../../network_config/" + config_N3["interruption"]
        source_IT_N4 = "../../network_config/" + config_N4["interruption"]
        source_IT_N5 = "../../network_config/" + config_N5["interruption"]
        dest_IT_N2 = config_N2["path"] + SOURCES + config_N2["interruption"]
        dest_IT_N3 = config_N3["path"] + SOURCES + config_N3["interruption"]
        dest_IT_N4 = config_N4["path"] + SOURCES + config_N4["interruption"]
        dest_IT_N5 = config_N5["path"] + SOURCES + config_N5["interruption"]

        copyfile(source_IT_N2, dest_IT_N2)
        copyfile(source_IT_N3, dest_IT_N3)
        copyfile(source_IT_N4, dest_IT_N4)
        copyfile(source_IT_N5, dest_IT_N5)

        ci_log.step_log(f"PlatformIO projects", "Step")
        # Update platformio.ini Build Flags
        replacetext(eval(f"config_N2[\"path\"]") + "/platformio.ini", "node_config.h", "N2_node_config.h \n    -I ../../config/")
        replacetext(eval(f"config_N3[\"path\"]") + "/platformio.ini", "node_config.h", "N3_node_config.h \n    -I ../../config/")
        replacetext(eval(f"config_N4[\"path\"]") + "/platformio.ini", "node_config.h", "N4_node_config.h \n    -I ../../config/")
        replacetext(eval(f"config_N5[\"path\"]") + "/platformio.ini", "node_config.h", "N5_node_config.h \n    -I ../../config/")

        # Update upload parameters in platformio.ini
        set_upload_command("N2")
        set_upload_command("N3")
        set_upload_command("N4")
        set_upload_command("N5")

        # Add break boards Power ON in projects
        replacetext(eval(f"config_N2[\"path\"]/src/main.c", "\/\* USER CODE END 2 \*\/", "HAL_Platform_Init();")
        replacetext(eval(f"config_N3[\"path\"]/src/main.c", "\/\* USER CODE END 2 \*\/", "HAL_Platform_Init();")
        replacetext(eval(f"config_N4[\"path\"]/src/main.c", "\/\* USER CODE END 2 \*\/", "HAL_Platform_Init();")
        replacetext(eval(f"config_N5[\"path\"]/src/main.c", "\/\* USER CODE END 2 \*\/", "HAL_Platform_Init();")

        # Upload all nodes
        # ######################################
        ci_log.phase_log('Setup MCUs')
        # ######################################
        platform= setup_nodes(__file__, network_conf, upload)   

        # Detection
        # ######################################
        ci_log.phase_log('Verify that Gate detect all nodes in bootloader mode')
        # ######################################

        ci_log.step_log(f"Detection", "Step")
        result, _ = platform.luos.ask_detections(delay=0.5)
        platform.engine.assert_step(result, "Detection OK")

        # Check Versions
        ci_log.step_log(f"Check Luos engine version", "Step")
        platform.luos.get_luos_versions("Gate")
        platform.luos.get_luos_versions("boot_1")
        platform.luos.get_luos_versions("boot_2")
        platform.luos.get_luos_versions("boot_3")
        time.sleep(0.1)

        # Verify topology
        # ############################################################################
        ci_log.phase_log(f'Verify topology : all nodes are in bootloader mode')
        # ############################################################################
        ci_log.step_log(services, "Services")
        services = platform.luos.device.services
        ci_log.step_log(nodes, "Nodes")
        nodes = platform.luos.device.nodes
        ci_log.step_log(f"Verify topology", "Step")
        platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_bootloader_topology, expected_bootloader_services), True)

        # Setup APP projects
        # ######################################
        ci_log.phase_log('Setup APP projects')
        # ######################################

        # Init project paths
        config_N2["path"] = path_config_N2
        config_N3["path"] = path_config_N2
        config_N4["path"] = path_config_N2
        config_N5["path"] = path_config_N2

        # Select App projects for nodes
        ci_log.step_log(f"Flash Gate and other nodes with bootloader", "Step")
        if gate_node == 2:
            config_N2["path"] += "gate_serialcom"
            config_N3["path"] += "led"
            config_N4["path"] += "dc_motor"
            config_N5["path"] += "potentiometer"
        if gate_node == 3: 
            config_N2["path"] += "button"
            config_N3["path"] += "gate_serialcom"
            config_N4["path"] += "dc_motor"
            config_N5["path"] += "potentiometer"
        if gate_node == 4: 
            config_N2["path"] += "button"
            config_N3["path"] += "led"
            config_N4["path"] += "gate_serialcom"
            config_N5["path"] += "potentiometer"
        if gate_node == 5: 
            config_N2["path"] += "button"
            config_N3["path"] += "led"
            config_N4["path"] += "dc_motor"
            config_N5["path"] += "gate_serialcom"

        ci_log.step_log(f"Interruptions configuration", "Step")
        dest_IT_N2 = config_N2["path"] + SOURCES + config_N2["interruption"]
        dest_IT_N3 = config_N3["path"] + SOURCES + config_N3["interruption"]
        dest_IT_N4 = config_N4["path"] + SOURCES + config_N4["interruption"]
        dest_IT_N5 = config_N5["path"] + SOURCES + config_N5["interruption"]
        copyfile(source_IT_N2, dest_IT_N2)
        copyfile(source_IT_N3, dest_IT_N3)
        copyfile(source_IT_N4, dest_IT_N4)
        copyfile(source_IT_N5, dest_IT_N5)

        ci_log.step_log(f"PlatformIO projects", "Step")
        # Update platformio.ini Build Flags
        replacetext(eval(f"config_N2[\"path\"]") + "/platformio.ini", "node_config.h", "N2_node_config.h \n    -I ../../config/")
        replacetext(eval(f"config_N3[\"path\"]") + "/platformio.ini", "node_config.h", "N3_node_config.h \n    -I ../../config/")
        replacetext(eval(f"config_N4[\"path\"]") + "/platformio.ini", "node_config.h", "N4_node_config.h \n    -I ../../config/")
        replacetext(eval(f"config_N5[\"path\"]") + "/platformio.ini", "node_config.h", "N5_node_config.h \n    -I ../../config/")

        # Add break boards Power ON in projects
        replacetext(eval(f"config_N2[\"path\"]/src/main.c", "\/\* USER CODE END 2 \*\/", "HAL_Platform_Init();")
        replacetext(eval(f"config_N3[\"path\"]/src/main.c", "\/\* USER CODE END 2 \*\/", "HAL_Platform_Init();")
        replacetext(eval(f"config_N4[\"path\"]/src/main.c", "\/\* USER CODE END 2 \*\/", "HAL_Platform_Init();")
        replacetext(eval(f"config_N5[\"path\"]/src/main.c", "\/\* USER CODE END 2 \*\/", "HAL_Platform_Init();")


        # Flash Apps with bootloader
        # ######################################
        ci_log.phase_log('Flash Apps with Bootloader')
        # ######################################

        def searchFirmware(node): ICI ICI ICI
            config_N2["path"]
            config_N3["path"]
            config_N4["path"]
            config_N5["path"]
            for root, dir, files in os.walk(projects[node]):
                if "firmware.bin" in files:
                    firmware_1 = os.path.join(root, "firmware.bin")
                    break
    
        def getFirmwarePath(node):
            if node == 2:
                firmware_2 = ""
                firmware_3 = ""
                firmware_4 = ""
            elif node == 3:
                firmware_2 = ""
                firmware_3 = ""
                firmware_4 = ""
            elif node == 4:
                firmware_2 = ""
                firmware_3 = ""
                firmware_4 = ""
            elif node == 5:
                firmware_2 = ""
                firmware_3 = ""
                firmware_4 = ""
            return firm1, firm2, firm3

        firmware_2, firmware_3, firmware_4 = getFirmwarePath(gate_node)
        flash_node_1 = f"pyluos-bootloader flash -t 2 -b {firmware_2}"
        flash_node_2 = f"pyluos-bootloader flash -t 3 -b {firmware_3}"
        flash_node_3 = f"pyluos-bootloader flash -t 4 -b {firmware_4}"

        ci_log.step_log(f"Flash App 1 with bootloader", "Step")
        run_command(flash_node_1, timeout= 50)
        ci_log.step_log(f"Flash App 2 with bootloader", "Step")
        run_command(flash_node_2, timeout= 50)
        ci_log.step_log(f"Flash App 3 with bootloader", "Step")
        run_command(flash_node_3, timeout= 50)

        # Detection
        # ######################################
        ci_log.phase_log('Verify that Gate detect all nodes in App mode')
        # ######################################

        ci_log.step_log(f"Detection", "Step")
        result, _ = platform.luos.ask_detections(delay=0.5)
        platform.engine.assert_step(result, "Detection OK")

        # Check Versions
        ci_log.step_log(f"Check Luos engine version", "Step")
        platform.luos.get_luos_versions("Gate")
        time.sleep(0.1)

        try:
            platform.luos.get_luos_versions("button")
        time.sleep(0.1)
        except:
            pass
        try:
            platform.luos.get_luos_versions("led")
        time.sleep(0.1)
        except:
            pass
        try:
            platform.luos.get_luos_versions("dc_motor")
        time.sleep(0.1)
        except:
            pass
        try:
            platform.luos.get_luos_versions("potentiometer")
        except:
            pass
        time.sleep(0.1)

        # Verify topology
        # ############################################################################
        ci_log.phase_log(f'Verify topology : all nodes must be in App mode')
        # ############################################################################
        ci_log.step_log(services, "Services")
        services = platform.luos.device.services
        
        ci_log.step_log(nodes, "Nodes")
        nodes = platform.luos.device.nodes
        
        ci_log.step_log(f"Verify topology", "Step")
        expected_topology = eval(f"expected_topology_N{gate_node}")
        expected_services = eval(f"expected_services_N{gate_node}")
        platform.engine.assert_step(platform.luos.verify_topology(nodes, expected_topology, expected_services), True)


if __name__ == '__main__':
    platform_handler, state, upload = get_arguments()
    try:
        platform = run_scenario()
    except Exception as e:
        scenario_exception(e)
        state= "Exception"
    finally:
        teardown(state, platform_handler)        
