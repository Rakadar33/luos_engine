# coding:utf-8
import time
from subprocess import Popen, PIPE
from tools.pytest_luos.termcolor import colored
from tools.pytest_luos.config.settings import *

class Engine:
    def __init__(self):
        self.error_counter = 0
        self.debug= False
        
    def assert_step(self, obtained, expected, message="", stop_on_failure=False):
        try:
            assert(obtained == expected)
        except:
            ci_log.logger.info(colored("\n[Step KO]", "red"))
            ci_log.logger.critical(colored(f"\n[Step KO]\t{message} : \"{obtained}\" instead of \"{expected}\"", "magenta"))
            pass

            if(stop_on_failure):
                time.sleep(0.1)
                raise Exception("[CRITICAL ERROR ON STEP : stop test]")
            else:
                self.error_counter += 1
                pass

    def test_result(self):
        ci_log.phase_log("End of test")
        if(self.error_counter == 0):
            ci_log.logger.info(colored("\n\n\n\t\t[SUCCEED]\t*** Test is OK ***\n\n", "green"))
            error = 0
        elif (self.error_counter == -1):
            ci_log.logger.info(colored("\n\n\n\t\t[UNEXPECTED ERROR]\t*** The test scenario doesn\'t handle this error ***\n\n", "magenta"))
            self.assert_step("[UNEXPECTED ERROR] the test scenario doesn\'t handle this error", "OK")
            error = -1
        else:
            if self.error_counter == 1:
                ci_log.logger.critical(colored(f"\n\n\n\t\t[FAILED]\t*** Test is KO: {self.error_counter} step is KO ***\n\n", "magenta"))
            else:
                ci_log.logger.critical(colored(f"\n\n\n\t\t[FAILED]\t*** Test is KO: {self.error_counter} steps are KO ***\n\n", "magenta"))
            error = -2
        sep= 30*"*" 
        ci_log.logger.info(colored(f"\n\n{sep}\nLogs are available in file:\n{sep}\n{ci_log.get_log_filename()}\n\n", "blue"))
        return error

    # Tools functions
    def teardown_step(self, cmd, message=""):
        ci_log.phase_log(f"Teardown : {message}")
        try:
            cmd
        except:
            ci_log.logger.error(message, "Teardown Step KO")
            pass

    def debug_breakpoint(self, force_breakpoint=False, message=''):
        if (self.debug == "ON") or (force_breakpoint == True):
            ci_log.logger.info(f"\n\t*** BREAKPOINT ***  {message}")
            time.sleep(0.1)
            input("\n")

    def FATAL(self, msg="Fatal Error for Debug"):
        ci_log.logger.critical(colored(msg, "magenta"))
        assert("FATAL" == msg)

    def debug_state(self, enable):
        if enable:
            self.debug= True
        else:
            self.debug= False

# Misc functions
def run_command(cmd, verbose=False, timeout=20):
    #cmd += ' 2>&1'
    process = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
    output, errors = process.communicate(timeout=timeout)
    if process.returncode:
        ci_log.logger.info(f"Return code : {process.returncode}")
        ci_log.logger.info(f"Error : {errors}")
        result = "ERROR"
    else:
        result = str(output)[2:-1]
        result = result.split("\\n")

    if verbose == True:
        ci_log.logger.info(f"--> Run command: {cmd}\n")
        ci_log.logger.info("--> Command returns: ")
        for line in result:
            ci_log.logger.info(line)
            pass
    return result
