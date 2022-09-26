# coding:utf-8
from tools.pytest_luos.test_engine import run_command


class HubControl:
    def __init__(self, type):
        self.type  = type

    def enable(self, port):
        if self.type =="default":
            self._enable_default(port)
        elif self.type =="capable_robot":            
            self._enable_capable_robot(port)

    def disable(self, port):
        if self.type =="default":
            self._disable_default(port)
        elif self.type =="capable_robot":            
            self._disable_capable_robot(port)

    # Private methods
    def _get_location(self, position):
        HUB= {"Port_1":  {"location": "2-1",     "port": "3"},
              "Port_3":  {"location": "2-1",     "port": "1"},
              "Port_8":  {"location": "2-1.4.4", "port": "2"},
              "Port_9":  {"location": "2-1.4.4", "port": "1"},
              "Port_10": {"location": "2-1.4.4", "port": "4"},
              "Port_5":  {"location": "4-1.4",   "port": "3"},
              }

        location= HUB[f"Port_{position}"]["location"]
        port= HUB[f"Port_{position}"]["port"]
        return location, port

    def _enable_default(self, port):
        if (port!= 0) and (port<= 10):
            #print(f"Power ON MCU on port {port}")
            location, port = self._get_location(port)
            start_command = f"sudo uhubctl -a on -p {port} -l {location};"
            start_command += f"echo 1 > sudo tee /sys/bus/usb/devices/{location}.{port}/authorized;"
            run_command(start_command)

    def _disable_default(self, port):
        if (port!= 0) and (port<= 10):
            #print(f"Power OFF MCU on HUB port {port}")
            location, port = self._get_location(port)            
            stop_command = f"echo 0 > sudo tee /sys/bus/usb/devices/{location}.{port}/authorized;"        
            stop_command += f"sudo uhubctl -a off -r 100 -l {location} -p {port};"
            run_command(stop_command)

    def _enable_capable_robot(self, port):
        #TODO
        pass

    def _disable_capable_robot(self, port):
        #TODO
        '''
        sudo cp 50-capablerobot-usbhub.rules /etc/udev/rules.d/
        sudo udevadm control --reload
        sudo udevadm trigger
        '''

        '''
            PS D:\\> usbhub

                Usage: usbhub [OPTIONS] COMMAND [ARGS]...

                Options:
                --hub TEXT     Numeric index or key (last 4 characters of serial number) or
                                USB path ('bus-address') of Hub for command to operate on.

                --verbose      Increase logging level.
                --disable-i2c  Disable I2C bus access.
                --help         Show this message and exit.

                Commands:
                data   Sub-commands for data control & monitoring
                id     Print serial number for attached hub
                power  Sub-commands for power control & monitoring
        '''

        '''
        #-------------------------------------------------------------------------------
        # import os, sys, inspect
        import time
        import logging
        import argparse
        #import capablerobot-usbhub
        import capablerobot-usbhub as capablerobot


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
            try:
                parser = argparse.ArgumentParser()
                parser.add_argument('--port', type=int)
                parser.add_argument('--power', type=str)
                args = parser.parse_args()
            except:
                raise Exception("Parameter : \n\t\
                                --port   Hub_Port_Number\n\t\
                                --power  ON or OFF")
            try:
                assert(args.port<5)
            except:
                print("\n\t*** ERROR: Forbidden port\n\t*** Possible values =  1 - 2 - 3 or 4\n")

            # --------------------
            # Control power
            # --------------------
            try:
                hub = capablerobot_usbhub.USBHub()
            except:
                print("\n\t*** Error : Unable to connect to Capable Robot USB Hub\n")
                sys.exit(1)

            if(arg.power == 'ON'):
                logger.info("Enable port %d" % args.port)
                hub.power.enable([port])
                time.sleep(0.5)
                sys.exit(0)

            elif(arg.power == 'OFF'):
                logger.info("Disable port %d" % args.port)
                hub.power.disable([port])
                time.sleep(0.5)
                sys.exit(0)
            logger.error(f"Unknwown power : {args.power}")
            sys.exit(2)
        '''
        pass
