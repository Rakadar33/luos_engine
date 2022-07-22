# -*- coding: utf-8 -*-
import os

# Instanciate Logger
if not "ci_log" in globals():
    from tools.pytest_luos.logger_engine import loggerEngine
    ci_log = loggerEngine()

# External softwares
stlink_detect = "st-info --probe"
stlink_flash = "st-flash --reset --serial $SERIAL write $PROJECT/.pio/build/$ENV/firmware.bin 0x8000000"
stlink_erase = "st-flash --serial $SERIAL erase"
openocd_path = "/home/luos_adm/.platformio/packages/tool-openocd/bin"
restart_mcu = f"{openocd_path}/openocd -f interface/stlink.cfg -f {openocd_path}/../scripts/target/$TARGET.cfg -c \"init; reset run; exit\""
halt_mcu = f"{openocd_path}/openocd -f interface/stlink.cfg -f {openocd_path}/../scripts/target/$TARGET.cfg -c \"init; reset halt; exit\""

# PlatformIO Env Variables
os.environ['PLATFORMIO_LIB_EXTRA_DIRS'] = "/var/www/PF/"
os.environ['PROJECT_PACKAGES_DIR'] = "/home/luos_adm/.platformio/packages"
