import os, sys, inspect
import time
import logging
import argparse
import capablerobot_usbhub as usbhub

lib_folder = os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0], '..')
lib_load = os.path.realpath(os.path.abspath(lib_folder))

if lib_load not in sys.path:
    sys.path.insert(0, lib_load)

FORMAT = '%(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('USB Hub Status')
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # --------------------
    # Arguments parsing
    # --------------------
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str)
    parser.add_argument('--power', type=str)
    args = parser.parse_args()

    power= args.power
    if (args.port is None):
        print("Parameters : \
                \n\t--port   Possible values for port=  1 - 2 - 3 - 4 or ALL\
                \n\t--power  ON or OFF")
        sys.exit(1)
    elif args.port == "ALL":
        allPorts = 1
    else:
        try:
            allPorts = 0
            port= int(args.port)
            assert(port != 0)
            assert(port <= 4)            
        except:
            print("Parameters : \
                    \n\t--port   Possible values for port=  1 - 2 - 3 - 4 or ALL\
                    \n\t--power  ON or OFF")
            sys.exit(2)

    # --------------------
    # Control power
    # --------------------
    device_kwargs={"disable_i2c": True}
    try:
        hub = usbhub.USBHub(device=device_kwargs)
    except Exception as e:
        logger.exception("Exception Occured while code Execution: "+ str(e))
        print("\n\n\t*** Error : Unable to connect to Capable Robot USB Hub\n")
        sys.exit(3)

    if(power == 'ON'):
        if(allPorts == 1):
            logger.info("Enable ALL ports")
            hub.power.enable([1,2,3,4])
        else:    
            logger.info("Enable port %d" % port)
            hub.power.enable([port])
        time.sleep(0.5)
        sys.exit(0)

    elif(power == 'OFF'):
        if(allPorts == 1):    
            logger.info("Disable ALL ports")
            hub.power.disable([1,2,3,4])
        else:    
            logger.info("Disable port %d" % port)
            hub.power.disable([port])
        time.sleep(0.5)
        sys.exit(0)

    logger.error(f"Unknown power : {power}")
    sys.exit(4)
