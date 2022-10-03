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
        pass