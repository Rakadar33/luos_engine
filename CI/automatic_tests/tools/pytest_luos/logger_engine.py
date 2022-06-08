# coding:utf-8
import os
import sys
import logging.config
import pprint as pp
from pathlib import Path
from termcolor import colored
from datetime import datetime
from functools import wraps


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


@singleton
class loggerEngine:
    # LEVEL Order : DEBUG,INFO,WARNING,ERROR,CRITICAL
    # Default LEVEL =  WARNING (ie show only WARNING + ERROR + CRITICAL)
    default_log_config = os.path.join(os.path.dirname(__file__), 'logger_engine.json')


    def __init__(self, log_config=default_log_config):
        # Create Log File directory
        # ------------------------------
        now=datetime.now()
        timestamp=now.strftime("%Y_%m_%d__%H:%M:%S")
        logPath=f"{Path(__file__).parent.resolve()}/../Results"
        self.logFileName=f"{logPath}/test_result.log"        
        os.makedirs(logPath, exist_ok=True)

        # Logging parameters
        # ------------------------------
        logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        datefmt = "%m-%d %H:%M"

        logging.basicConfig(filename=self.logFileName, level=logging.INFO, filemode="w", format=logformat, datefmt=datefmt)
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(logging.Formatter(fmt=logformat, datefmt=datefmt))

        # Logging creation
        # ------------------------------
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(stream_handler)
        self.pp = pp.PrettyPrinter(indent=4)
        self.logger.warning(f"\n\n----- NEW LOG INSTANCE : {timestamp} -----\n"+51*"-")        

    def get_log_filename(self):
        return self.logFileName
        
    def pretty_print(self, msg):
        self.pp.pprint("\n"+msg)
        self.logger("\n"+msg)

    def phase_print(self, title, message=""):    
        self.logger.info(colored(f"\n{10*'-'}{title}{10*'-'}","red"))
        #self.logger.info(f"{10*'-'}{title}{10*'-'}")
        if message != "":
            self.logger.info(colored(f"\n{message}","yellow"))
            #self.logger.info(message)

    def step_print(self, message, title=""):
        if title != "":
            self.logger.info(colored(f"\n{10*'-'}{title}{10*'-'}","blue"))
            #self.logger.info(f"{10*'-'}{title}{10*'-'}")
        self.logger.info(colored(f"\n{message}","blue"))
        #self.logger.info(message)

    def colored_print(self, message, color="yellow"):
        # Availabled colors : grey,  red,  green,  yellow,  blue,  magenta,  cyan,  white
        self.logger.info(colored(f"\n{message}",color))

# ----------------------
# Logger Initialisation
# ----------------------
def log_init():
    global log
    #log_file = os.path.join(os.path.dirname(__file__), 'logging_configuration.json')
    log = loggerEngine(os.path.join(os.path.dirname(__file__), 'logging_configuration.json'))
    log.logger.info("Start logging")
