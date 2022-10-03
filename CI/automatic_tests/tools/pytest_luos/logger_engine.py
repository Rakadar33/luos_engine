# coding:utf-8
from distutils.log import error, info
from logging import critical
from functools import wraps
import os
import sys
import logging.config
import pprint as pp
from pathlib import Path
from tools.pytest_luos.termcolor import colored
from datetime import datetime

def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls)
        return instance
    orig_cls.__new__ = __new__
    return orig_cls

class loggerSingleton:
    '''
    # -----------------------------------------------------------------------
    # LEVEL Order : DEBUG,INFO,WARNING,ERROR,CRITICAL
    #
    # Default LEVEL =  WARNING (ie show only WARNING + ERROR + CRITICAL)
    # -----------------------------------------------------------------------    
    '''
    default_log_config = os.path.join(os.path.dirname(__file__), 'logger_engine.json')

    def __init__(self, log_config=default_log_config):
        # Create Log File directory
        now=datetime.now()
        timestamp=now.strftime("%Y_%m_%d__%H:%M:%S")
        logPath=f"{Path(__file__).parent.resolve()}/../../Results"
        self.logFileName=f"{logPath}/test_result_{timestamp}.log"
        os.makedirs(logPath, exist_ok=True)

        # Logging parameters
        logformat = "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s"
        datefmt = "%m-%d %H:%M:%S"

        logging.basicConfig(filename=self.logFileName, level=logging.INFO, filemode="w", format=logformat, datefmt=datefmt)
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(logging.Formatter(fmt=logformat, datefmt=datefmt))

        # Logging creation
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(stream_handler)
        self.pp = pp.PrettyPrinter(indent=4)
        self.logger.warning(colored(f"\n\n----- NEW LOG INSTANCE {timestamp} -----\n" + 51*"-" + "\n","green"))

@singleton
class loggerEngine(loggerSingleton):
    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__), 'logging_configuration.json'))

    def log(self,type, message):
        if type == "info":
            self.logger.info(message)
        elif type == "warning":
            self.logger.warning(message)
        elif type == "critical":
            self.logger.critical(message)
        elif type == "error":
            self.logger.error(message)
        else:
            self.logger.error(f"Type \"{type}\" is unknown for message: \"{message}\"")

    def get_log_filename(self):
        return self.logFileName
        
    def pretty_print(self, msg):
        self.pp.pprint("\n"+msg)
        self.logger("\n"+msg)

    def phase_log(self, title, message=""):    
        self.logger.info(colored(f"\n{10*'-'}{title}{10*'-'}","green"))
        if message != "":
            self.logger.info(colored(f"\n{message}","yellow"))
    def step_log(self, message, title=""):
        #'''
        if title != "":
            self.logger.info(colored(f"\n{10*'-'}{title}{10*'-'}","blue"))
        self.logger.info(colored(f"\n{message}","blue"))

    def colored_log(self, message, color="yellow"):
        # Availabled colors : grey,  red,  green,  yellow,  blue,  magenta,  cyan,  white
        self.logger.info(colored(f"\n{message}",color))
