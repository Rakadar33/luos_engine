# -*- coding: utf-8 -*-
import time
from multiprocessing import cpu_count
from termcolor import colored
#from platformio import fs
#from platformio.platform.factory import PlatformFactory
#from platformio.project.config import ProjectConfig
#from Parameters import *
from subprocess import Popen, PIPE
import pytest_luos.hub_controller as HUB
import pytest_luos.luos_controller as LUOS
import pytest_luos.mcu_controller as MCU

class LuosPytest:
    def __init__(self):
        self.engine = Engine()
        self.luos = LUOS.LuosControl()
        self.mcu = MCU.McuControl()
        self.basic_hub = HUB.HubControl("default")
        self.prog_hub = HUB.HubControl("capable_robot")

class Engine:
    def assert_step(self, obtained, expected, message="", stop_on_failure=False):
        try:
            assert(obtained == expected)
        except:
            log.logger.info(colored("\n[Step KO]", "red"))
            log.logger.critical(
                f"\n[Step KO]\t{message} : \"{obtained}\" instead of \"{expected}\"")
            pass

            if(stop_on_failure):
                time.sleep(0.1)
                raise Exception("[CRITICAL ERROR ON STEP : stop test]")
            else:
                self.error_counter += 1
                pass

    def test_result(self):
        log.phase_print("End of test")
        if(self.error_counter == 0):
            log.logger.info("\n\t--> Test is OK")
            error = 0
        elif (self.error_counter == -1):
            log.logger.warning("\n\t--> Error in test architecture")
            self.assert_step("Error in test architecture", "OK")
            error = -1
        else:
            log.logger.critical(
                f"\n\t--> Test is KO : {self.error_counter} step(s) KO")
            error = -2
        log.logger.info(
            f"\n\nLogs are available in file :\n{log.get_log_filename()}\n\n")
        return error

    # Tools functions
    def teardown_step(cmd, message=""):
        log.phase_print(f"Teardown : {message}")
        try:
            cmd
        except:
            log.logger.error(message, "Teardown Step KO")
            pass

    def debug_breakpoint(force_breakpoint=False, message=''):
        if (BREAKPOINT == "ON") or (force_breakpoint == True):
            log.logger.info(f"\n\t*** BREAKPOINT ***  {message}")
            time.sleep(0.1)
            input("\n")

    def FATAL(msg="Fatal Error for Debug"):
        log.logger.critical(msg)
        assert("FATAL" == msg)


class Tools:
    def __init__(self):
        pass

    def run_command(self, cmd, verbose=False):
        #cmd += ' 2>&1'
        process = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
        output, errors = process.communicate()

        # if process.returncode or errors:
        if process.returncode:
            #TODO LOG
            # log.logger.info(f"Return code : {process.returncode}")
            #log.logger.info(f"Error : {errors}")
            result = "ERROR"
        else:
            result = str(output)[2:-1]
            result = result.split("\\n")

        if verbose == True:
            #TODO LOG            
            #log.logger.info(f"--> Run command: {cmd}\n")
            #log.logger.info("--> Command returns: ")
            for line in result:
                #log.logger.info(line)
                pass
        return result
