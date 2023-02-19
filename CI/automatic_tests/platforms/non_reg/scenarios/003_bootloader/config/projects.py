# coding:utf-8
import os
import sys
import glob
from shutil import copyfile, copytree, rmtree
from pyluos import Device
from tools.pytest_luos.config.settings import ci_log
from tools.pytest_luos.config.platform import create_platform
from tools.pytest_luos.test_engine import run_command
from platforms.non_reg.network_config.config import NetworkNodeConfig
from platforms.non_reg.scenario_tools import *
from config.parameters import *

def product_config_bootloader(gate_node, tested_version = "main"):
    # Setup projects
    ci_log.phase_log('Setup BOOTLOADER projects')

    # Clone luos engine
    ci_log.step_log(f"Clone Luos engine", "Step")
    if os.path.isdir('luos_engine'):
        try:
            #ci_log.logger.warning(f"Remove Luos Engine directory")
            for root, dirs, files in os.walk("luos_engine", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.removedirs("luos_engine")
        except:
            error = "Unable to remove Luos Engine directory"
            ci_log.logger.warning(error)
    cmd = "git clone https://github.com/Luos-io/luos_engine.git"
    assert(run_command(cmd, verbose=False, timeout=20) != "ERROR")
    cmd = f"cd luos_engine;git checkout {tested_version}"
    assert(run_command(cmd, verbose=False, timeout=20) != "ERROR")

    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    '''replacetext("./luos_engine/source_filter_script.py", "\$PYTHONEXE -m pip install", "echo")
    cmd = "pip3 uninstall pyluos -y"
    assert(run_command(cmd, verbose=False, timeout=20) != "ERROR")
    cmd = "pip3 install -e /var/www/PF/Workspace/Pyluos"
    assert(run_command(cmd, verbose=False, timeout=20) != "ERROR")'''
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!

    # Local libraries
    libs = glob.glob("./luos_engine/**/library.json", recursive = True)
    for lib in libs:
        replacetext(lib, "luos/luos_engine", "luos_engine")

    # Select Gate & Bootloaders projects for nodes
    global config_N2, config_N3, config_N4, config_N5     
    if gate_node == 2: 
        config_N2["path"] = config_N2["path_gate"]
        config_N3["path"] = config_N3["path_bootloader"]
        config_N4["path"] = config_N4["path_bootloader"]
        config_N5["path"] = config_N5["path_bootloader"]
    elif gate_node == 3: 
        config_N3["path"] = config_N3["path_gate"]
        config_N2["path"] = config_N2["path_bootloader"]
        config_N4["path"] = config_N4["path_bootloader"]
        config_N5["path"] = config_N5["path_bootloader"]
    elif gate_node == 4: 
        config_N4["path"] = config_N4["path_gate"]
        config_N2["path"] = config_N2["path_bootloader"]
        config_N3["path"] = config_N3["path_bootloader"]
        config_N5["path"] = config_N5["path_bootloader"]
    elif gate_node == 5: 
        config_N5["path"] = config_N5["path_gate"]
        config_N2["path"] = config_N2["path_bootloader"]
        config_N3["path"] = config_N3["path_bootloader"]
        config_N4["path"] = config_N4["path_bootloader"]

    ci_log.step_log(f"Interruptions configuration", "Step")
    SOURCES = "/src/"
    source_IT_N2 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N2["interruption"]
    source_IT_N3 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N3["interruption"]
    source_IT_N4 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N4["interruption"]
    source_IT_N5 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N5["interruption"]
    dest_IT_N2 = config_N2["path"] + SOURCES + config_N2["interruption"]
    dest_IT_N3 = config_N3["path"] + SOURCES + config_N3["interruption"]
    dest_IT_N4 = config_N4["path"] + SOURCES + config_N4["interruption"]
    dest_IT_N5 = config_N5["path"] + SOURCES + config_N5["interruption"]

    copyfile(source_IT_N2, dest_IT_N2)
    copyfile(source_IT_N3, dest_IT_N3)
    copyfile(source_IT_N4, dest_IT_N4)
    copyfile(source_IT_N5, dest_IT_N5)

    def set_upload_command(config):
        ci_log.step_log(f"Setup PlatformIO bootloader projects", "Step")
        project_config_file= eval(f"config_{config}[\"path\"]") +  "/platformio.ini"
        replacetext(project_config_file, "upload_protocol", ";upload_protocol") 
        replacetext(project_config_file, "upload_flags", ";upload_flags") 
        replacetext(project_config_file, "upload_command", ";command") 
        replacetext(project_config_file, "upload_protocol", ";upload_protocol")
        #replacetext(project_config_file, "debug_build_flags", ";debug_build_flags")
        replacetext(project_config_file, "\$PROJECT_DIR", ";") 
        replacetext(project_config_file, "-t", ";-t")

        target_config = eval(f"config_{config}['flashing_options']['config']")
        serial = eval(f"config_{config}['flashing_options']['serial']")
        upload_params = '\n' +\
                        'upload_protocol = custom\n'+\
                        'upload_command = openocd -s $PROJECT_PACKAGES_DIR/tool-openocd/scripts -f interface/stlink.cfg -c "transport select hla_swd" $UPLOAD_FLAGS -c "program {$SOURCE} 0x08000000 verify reset; shutdown;"\n'+\
                        'upload_flags =\n'+\
                        '\t-c\n'+\
                        f'\thla_serial {serial}\n'+\
                        '\t-f\n'+\
                        f'\ttarget/{target_config}\n'
        replacetext(project_config_file, "\[env\]", "[env]" + upload_params) 
        with open(project_config_file, "a+") as f:
            f.write('\n')
            f.write('upload_protocol = custom\n')
            f.write('upload_command = openocd -s $PROJECT_PACKAGES_DIR/tool-openocd/scripts -f interface/stlink.cfg -c "transport select hla_swd" $UPLOAD_FLAGS -c "program {$SOURCE} 0x08000000 verify reset; shutdown;"\n')
            f.write('upload_flags =\n')
            f.write('\t-c\n')
            f.write(f'\thla_serial {serial}\n')
            f.write('\t-f\n')
            f.write(f'\ttarget/{target_config}\n')

    # Update Build Flags in platformio.ini
    replacetext(config_N2["path"] + "/platformio.ini", "node_config.h", "N2_node_config.h \n    -I ../../../../../config/\n    -DNOTELEMETRY")
    replacetext(config_N3["path"] + "/platformio.ini", "node_config.h", "N3_node_config.h \n    -I ../../../../../config/\n    -DNOTELEMETRY")
    replacetext(config_N4["path"] + "/platformio.ini", "node_config.h", "N4_node_config.h \n    -I ../../../../../config/\n    -DNOTELEMETRY")
    replacetext(config_N5["path"] + "/platformio.ini", "node_config.h", "N5_node_config.h \n    -I ../../../../../config/\n    -DNOTELEMETRY")
    # Update Luos Engine version in platformio.ini
    luos_engine_version= f";https://github.com/Luos-io/luos_engine.git#{tested_version}\n\t;"
    replacetext(config_N2["path"] + "/platformio.ini", "luos_engine", luos_engine_version)
    replacetext(config_N3["path"] + "/platformio.ini", "luos_engine", luos_engine_version)
    replacetext(config_N4["path"] + "/platformio.ini", "luos_engine", luos_engine_version)
    replacetext(config_N5["path"] + "/platformio.ini", "luos_engine", luos_engine_version)
    # Update upload parameters in platformio.ini
    set_upload_command("N2")
    set_upload_command("N3")
    set_upload_command("N4")
    set_upload_command("N5")

    replacetext(config_N2["path"] + "/platformio.ini", "lib_extra_dirs = ;/", "lib_extra_dirs = ./")
    replacetext(config_N3["path"] + "/platformio.ini", "lib_extra_dirs = ;/", "lib_extra_dirs = ./")
    replacetext(config_N4["path"] + "/platformio.ini", "lib_extra_dirs = ;/", "lib_extra_dirs = ./")
    replacetext(config_N5["path"] + "/platformio.ini", "lib_extra_dirs = ;/", "lib_extra_dirs = ./")

    replacetext(config_N2["path"] + "/platformio.ini", ";/../../../../tool_services/", "./../../../../tool_services/")
    replacetext(config_N3["path"] + "/platformio.ini", ";/../../../../tool_services/", "./../../../../tool_services/")
    replacetext(config_N4["path"] + "/platformio.ini", ";/../../../../tool_services/", "./../../../../tool_services/")
    replacetext(config_N5["path"] + "/platformio.ini", ";/../../../../tool_services/", "./../../../../tool_services/")
    
    replacetext(config_N2["path"] + "/platformio.ini", ";/../../../../../", "./../../../../../")
    replacetext(config_N3["path"] + "/platformio.ini", ";/../../../../../", "./../../../../../")
    replacetext(config_N4["path"] + "/platformio.ini", ";/../../../../../", "./../../../../../")
    replacetext(config_N5["path"] + "/platformio.ini", ";/../../../../../", "./../../../../../")

    # Add HAL platform initialisation in projects
    default_pattern  = "HAL_Init\(\);"
    init_breakboards = "HAL_Init();\n\tHAL_Platform_Init();"
    replacetext(config_N2["path"] + SOURCES + "main.c", default_pattern, init_breakboards)
    replacetext(config_N3["path"] + SOURCES + "main.c", default_pattern, init_breakboards)
    replacetext(config_N4["path"] + SOURCES + "main.c", default_pattern, init_breakboards)
    replacetext(config_N5["path"] + SOURCES + "main.c", default_pattern, init_breakboards)
    default_pattern  = "LuosBootloader_Init\(\);"
    init_breakboards = "LuosBootloader_Init();\n\tHAL_Platform_Init();"
    replacetext(config_N2["path"] + "/../../../../engine/core/src/luos_engine.c", default_pattern, init_breakboards)


def product_config_apps(gate_node, tested_version= "main"):
    ci_log.phase_log('Setup APP projects')

    # Clone luos engine
    ci_log.step_log(f"Clone Luos engine", "Step")
    if os.path.isdir('luos_engine'):
        try:
            #ci_log.logger.warning(f"Remove Luos Engine directory")
            for root, dirs, files in os.walk("luos_engine", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.removedirs("luos_engine")
        except:
            error = "Unable to remove Luos Engine directory"
            ci_log.logger.warning(error)
    cmd = "git clone https://github.com/Luos-io/luos_engine.git"
    assert(run_command(cmd, verbose=False, timeout=20) != "ERROR")
    cmd = f"cd luos_engine;git checkout {tested_version}"
    assert(run_command(cmd, verbose=False, timeout=20) != "ERROR")

    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    '''replacetext("./luos_engine/source_filter_script.py", "\$PYTHONEXE -m pip install", "echo")
    cmd = "pip3 uninstall pyluos -y"
    run_command(cmd, verbose=False, timeout=20)
    cmd = "pip3 install -e /var/www/PF/Workspace/Pyluos"
    assert(run_command(cmd, verbose=False, timeout=20) != "ERROR")'''
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!
    # DEBUG HACK !!!!!!!!!!!!!!!!!!!!!!!!!!

    # Local libraries
    libs = glob.glob("./luos_engine/**/library.json", recursive = True)
    for lib in libs:
        replacetext(lib, "luos/luos_engine", "luos_engine")

    # Select Gate & Apps projects for nodes
    global config_N2, config_N3, config_N4, config_N5 
    if gate_node == 2: 
        config_N2["path"] = config_N2["path_gate"]
        config_N3["path"] = config_N3["path_app"]
        config_N4["path"] = config_N4["path_app"]
        config_N5["path"] = config_N5["path_app"]
    elif gate_node == 3: 
        config_N3["path"] = config_N3["path_gate"]
        config_N2["path"] = config_N2["path_app"]
        config_N4["path"] = config_N4["path_app"]
        config_N5["path"] = config_N5["path_app"]
    elif gate_node == 4: 
        config_N4["path"] = config_N4["path_gate"]
        config_N2["path"] = config_N2["path_app"]
        config_N3["path"] = config_N3["path_app"]
        config_N5["path"] = config_N5["path_app"]
    elif gate_node == 5: 
        config_N5["path"] = config_N5["path_gate"]
        config_N2["path"] = config_N2["path_app"]
        config_N3["path"] = config_N3["path_app"]
        config_N4["path"] = config_N4["path_app"]
 
    ci_log.step_log(f"Interruptions configuration", "Step")
    SOURCES = "/src/"
    source_IT_N2 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N2["interruption"]
    source_IT_N3 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N3["interruption"]
    source_IT_N4 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N4["interruption"]
    source_IT_N5 = f"{Path(__file__).parent.resolve()}/../../network_config/" + config_N5["interruption"]
    dest_IT_N2 = config_N2["path"] + SOURCES + config_N2["interruption"]
    dest_IT_N3 = config_N3["path"] + SOURCES + config_N3["interruption"]
    dest_IT_N4 = config_N4["path"] + SOURCES + config_N4["interruption"]
    dest_IT_N5 = config_N5["path"] + SOURCES + config_N5["interruption"]
    copyfile(source_IT_N2, dest_IT_N2)
    copyfile(source_IT_N3, dest_IT_N3)
    copyfile(source_IT_N4, dest_IT_N4)
    copyfile(source_IT_N5, dest_IT_N5)

    # Update platformio.ini Upload parameters)
    def set_upload_command(config):
        project_config_file= eval(f"config_{config}[\"path\"]") + "/platformio.ini"

        replacetext(project_config_file, "upload_protocol", ";upload_protocol") 
        replacetext(project_config_file, "upload_flags", ";upload_flags") 
        replacetext(project_config_file, "upload_command", ";command") 
        replacetext(project_config_file, "upload_protocol", ";upload_protocol") 
        replacetext(project_config_file, "\$PROJECT_DIR", ";") 
        replacetext(project_config_file, "-t", ";-t")

        target_config = eval(f"config_{config}['flashing_options']['config']")
        serial = eval(f"config_{config}['flashing_options']['serial']")

        upload_params = '\n' +\
                        'upload_protocol = custom\n'+\
                        'upload_command = openocd -s $PROJECT_PACKAGES_DIR/tool-openocd/scripts -f interface/stlink.cfg -c "transport select hla_swd" $UPLOAD_FLAGS -c "program {$SOURCE} 0x08000000 verify reset; shutdown;"\n'+\
                        'upload_flags =\n'+\
                        '\t-c\n'+\
                        f'\thla_serial {serial}\n'+\
                        '\t-f\n'+\
                        f'\ttarget/{target_config}\n'
        replacetext(project_config_file, "\[env\]", "[env]" + upload_params) 

        with open(project_config_file, "a+") as f:
            f.write('\n')
            f.write('upload_protocol = custom\n')
            f.write('upload_command = openocd -s $PROJECT_PACKAGES_DIR/tool-openocd/scripts -f interface/stlink.cfg -c "transport select hla_swd" $UPLOAD_FLAGS -c "program {$SOURCE} 0x08000000 verify reset; shutdown;"\n')
            f.write('upload_flags =\n')
            f.write('\t-c\n')
            f.write(f'\thla_serial {serial}\n')
            f.write('\t-f\n')
            f.write(f'\ttarget/{target_config}\n')

    # Update Build Flags in platformio.ini
    replacetext(config_N2["path"] + "/platformio.ini", "node_config.h", "N2_node_config.h \n    -I ../../../../../config/\n    -DNOTELEMETRY")
    replacetext(config_N3["path"] + "/platformio.ini", "node_config.h", "N3_node_config.h \n    -I ../../../../../config/\n    -DNOTELEMETRY")
    replacetext(config_N4["path"] + "/platformio.ini", "node_config.h", "N4_node_config.h \n    -I ../../../../../config/\n    -DNOTELEMETRY")
    replacetext(config_N5["path"] + "/platformio.ini", "node_config.h", "N5_node_config.h \n    -I ../../../../../config/\n    -DNOTELEMETRY")
    # Update Luos Engine version in platformio.ini
    luos_engine_version= f";https://github.com/Luos-io/luos_engine.git#{tested_version}\n\t;"
    replacetext(config_N2["path"] + "/platformio.ini", "luos_engine", luos_engine_version)
    replacetext(config_N3["path"] + "/platformio.ini", "luos_engine", luos_engine_version)
    replacetext(config_N4["path"] + "/platformio.ini", "luos_engine", luos_engine_version)
    replacetext(config_N5["path"] + "/platformio.ini", "luos_engine", luos_engine_version)
    # Update upload parameters in platformio.ini
    set_upload_command("N2")
    set_upload_command("N3")
    set_upload_command("N4")
    set_upload_command("N5")

    replacetext(config_N2["path"] + "/platformio.ini", "lib_extra_dirs = ;/", "lib_extra_dirs = ./")
    replacetext(config_N3["path"] + "/platformio.ini", "lib_extra_dirs = ;/", "lib_extra_dirs = ./")
    replacetext(config_N4["path"] + "/platformio.ini", "lib_extra_dirs = ;/", "lib_extra_dirs = ./")
    replacetext(config_N5["path"] + "/platformio.ini", "lib_extra_dirs = ;/", "lib_extra_dirs = ./")

    replacetext(config_N2["path"] + "/platformio.ini", ";/../../../../tool_services/", "./../../../../tool_services/")
    replacetext(config_N3["path"] + "/platformio.ini", ";/../../../../tool_services/", "./../../../../tool_services/")
    replacetext(config_N4["path"] + "/platformio.ini", ";/../../../../tool_services/", "./../../../../tool_services/")
    replacetext(config_N5["path"] + "/platformio.ini", ";/../../../../tool_services/", "./../../../../tool_services/")
    
    replacetext(config_N2["path"] + "/platformio.ini", ";/../../../../../", "./../../../../../")
    replacetext(config_N3["path"] + "/platformio.ini", ";/../../../../../", "./../../../../../")
    replacetext(config_N4["path"] + "/platformio.ini", ";/../../../../../", "./../../../../../")
    replacetext(config_N5["path"] + "/platformio.ini", ";/../../../../../", "./../../../../../")

    # Add HAL platform initialisation in projects
    default_pattern  = "Luos_Init\(\);"
    init_breakboards = "Luos_Init();\n\tHAL_Platform_Init();"
    replacetext(config_N2["path"] + SOURCES + "main.c", default_pattern, init_breakboards)
    replacetext(config_N3["path"] + SOURCES + "main.c", default_pattern, init_breakboards)
    replacetext(config_N4["path"] + SOURCES + "main.c", default_pattern, init_breakboards)
    replacetext(config_N5["path"] + SOURCES + "main.c", default_pattern, init_breakboards)

def getFirmwarePath(node):
    node = str(node)
    path = {}
    if node == '2': 
        path['firmware_2'] = config_N3["path_app"] + "/.pio/build/" + config_N3["target"] + "/firmware.bin"
        path['firmware_3'] = config_N4["path_app"] + "/.pio/build/" + config_N4["target"] + "/firmware.bin"
        path['firmware_4'] = config_N5["path_app"] + "/.pio/build/" + config_N5["target"] + "/firmware.bin"
        path['node_2'] = 2 #TODO 2/3/4
        path['node_3'] = 3 #TODO 2/3/4
        path['node_4'] = 4 #TODO 2/3/4
    elif node == '3':
        path['firmware_2'] = config_N2["path_app"] + "/.pio/build/" + config_N2["target"] + "/firmware.bin"
        path['firmware_3'] = config_N4["path_app"] + "/.pio/build/" + config_N4["target"] + "/firmware.bin"
        path['firmware_4'] = config_N5["path_app"] + "/.pio/build/" + config_N5["target"] + "/firmware.bin"
        path['node_2'] = 2 #TODO 2/3/4
        path['node_3'] = 3 #TODO 2/3/4
        path['node_4'] = 4 #TODO 2/3/4
    elif node == '4':
        path['firmware_2'] = config_N2["path_app"] + "/.pio/build/" + config_N2["target"] + "/firmware.bin"
        path['firmware_3'] = config_N3["path_app"] + "/.pio/build/" + config_N3["target"] + "/firmware.bin"
        path['firmware_4'] = config_N5["path_app"] + "/.pio/build/" + config_N5["target"] + "/firmware.bin"
        path['node_2'] = 2 #TODO 2/3/4
        path['node_3'] = 3 #TODO 2/3/4
        path['node_4'] = 4 #TODO 2/3/4
    elif node == '5':
        path['firmware_2'] = config_N2["path_app"] + "/.pio/build/" + config_N2["target"] + "/firmware.bin"
        path['firmware_3'] = config_N3["path_app"] + "/.pio/build/" + config_N3["target"] + "/firmware.bin"
        path['firmware_4'] = config_N4["path_app"] + "/.pio/build/" + config_N4["target"] + "/firmware.bin"
        path['node_2'] = 2 #TODO 2/3/4
        path['node_3'] = 3 #TODO 2/3/4
        path['node_4'] = 4 #TODO 2/3/4
    else:
        path['firmware_2'] = 'Unknown'
        path['firmware_3'] = 'Unknown'
        path['firmware_4'] = 'Unknown'
        path['node_2'] = -1
        path['node_3'] = -1
        path['node_4'] = -1

    return path
