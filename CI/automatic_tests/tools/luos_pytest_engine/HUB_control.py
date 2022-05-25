# coding:utf-8
import os
import sys
import argparse
from tools import stop_MCU, start_MCU
import tools

if __name__ == '__main__':    
    # --------------------
    # Arguments parsing
    # --------------------
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--hub', type=str, default="UNKNOWN")
        parser.add_argument('--port', type=int, default="0")        
        args = parser.parse_args()
    except:
        raise Exception("Usage : please enter parameter :\n\t\
                         --hub  ON or OFF")

    port = args.port
    hub  = args.hub
    

    if (port != 0) and (port <= 10):
        if hub == "ON":
            print("Enable HUB")
            start_MCU(port)
        elif hub == "OFF":
            print("Disable HUB")    
            stop_MCU(port)
        else:
            print("Unknown HUB parameter :  please enter parameter \"--hub  ON or OFF\" \"--port 0 to 10\"")
    else:
        print("Unknown PORT parameter :  please enter parameter \"--hub  ON or OFF\" \"--port 0 to 10\"")    


