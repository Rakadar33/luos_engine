# coding:utf-8
import os
import sys
from pathlib import Path

# PTP configs Matrix
# -------------------
#
#   Example:
#   ********
#
#       ["AB", "CD", "AC", "C", "None"] means:
#
#           - Node 1 (Arduino) is configured with PTP:    A    and    B
#           - Node 2 (F072-RB) is configured with PTP:    C    and    D
#           - Node 3 (F401-RE) is configured with PTP:    A    and    C
#           - Node 4 (L432-KC) is configured with PTP:    C
#           - Node 5 (G431-KB) PTP are disabled (electrically excluded from the network)
#
#
networkConfig={}
networkConfig["N1"] =             [None, None, None, None, None]
networkConfig["N2"] =             [None, None, None, None, None]
networkConfig["N3"] =             [None, None, None, None, None]
networkConfig["N4"] =             [None, None, None, None, None]
networkConfig["N5"] =             [None, None, None, None, None]
networkConfig["N1_N2"] =          ["A" , "A" , None, None, None]
networkConfig["N1_N3"] =          ["B" , None, "A" , None, None]
networkConfig["N1_N4"] =          ["C" , None, None, "A" , None]
networkConfig["N1_N5"] =          ["D" , None, None, None, "A" ]
networkConfig["N2_N3"] =          [None, "B" , "B" , None, None]
networkConfig["N2_N4"] =          [None, "C" , None, "B" , None]
networkConfig["N2_N5"] =          [None, "D" , None, None, "B" ]
networkConfig["N3_N4"] =          [None, None, "C" , "C" , None]
networkConfig["N3_N5"] =          [None, None, "D" , None, "C" ]
networkConfig["N4_N5"] =          [None, None, None, "D" , "D" ]
networkConfig["N1_N2_N3"] =       ["A" , "AB", "B" , None, None]
networkConfig["N2_N1_N3"] =       ["A" , "AB", "A" , None, None]
networkConfig["N1_N2_N4"] =       ["A" , "AC", None, "B" , None]
networkConfig["N1_N2_N5"] =       ["A" , "AD", None, None, "B" ]
networkConfig["N1_N3_N4"] =       ["B" , None, "AC", "C" , None]
networkConfig["N1_N3_N5"] =       ["B" , None, "AD", None, "C" ]
networkConfig["N1_N4_N5"] =       ["C" , None, None, "AD", "D" ]
networkConfig["N2_N3_N4"] =       [None, "B" , "BC", "C" , None]
networkConfig["N2_N3_N5"] =       [None, "B" , "BD", None, "C" ]
networkConfig["N2_N4_N5"] =       [None, "C" , None, "BD", "D" ]
networkConfig["N3_N4_N5"] =       [None, None, "C" , "CD", "C" ]
networkConfig["N1_N2_N3_N4"] =    ["A" , "AB", "BC", "C" , None]
networkConfig["N1_N2_N3_N5"] =    ["A" , "AB", "BD", None, "C" ]
networkConfig["N1_N2_N4_N5"] =    ["A" , "AC", None, "BD", "D" ]
networkConfig["N1_N3_N4_N5"] =    ["B" , None, "AC", "CD", "D" ]
networkConfig["N2_N3_N4_N5"] =    [None, "B",  "BC", "CD", "D" ]
networkConfig["N2_N1_N3_N4_N5"] = ["AB", "A" , "AC", "CD",  "D"]

class NetworkNodeConfig():
    def __init__(self, scenario_path, conf, max_node_number=5):
        self.scenario_name= self._get_scenario_name(scenario_path)
        self.max_node_number= max_node_number
        try:
            self.config= networkConfig[conf]
        except:
            invert_conf= conf.split("_")
            conf= f"{invert_conf[1]}_{invert_conf[0]}"
            self.config= networkConfig[conf]
            pass

    def nodeConfig_generation(self):
        status= True
        info = "\n"
        for node in range(self.max_node_number):
            source= f"{Path( __file__ ).parent.absolute()}/template_N{node+1}_node_config.h"
            destination= f"{Path( __file__ ).parent.absolute()}/../scenarios/{self.scenario_name}/config/N{node+1}_node_config.h"
            pattern= "#define PTP_CONFIG_UNKNOWN"
            new_config = f"#define PTP_CONFIG_{self.config[node]}"

            self._remove_config_files(node)
            try:
                # Compute node_config PTPs connection for
                template_file = open(source, 'r')
                data = template_file.read()
                if self.config[node] is not None:
                    print(f"\t\t\t\t{chr(664)} [Node {node+1}] PTP are connected to :  {self.config[node]}")
                    data = data.replace(pattern, new_config)
                else:
                    info+= f"\t\t\t\tx [Node {node+1}] is NOT connected to the network"
                template_file.close()
                # Create node_config.h
                node_config_file = open(destination, 'x')
                node_config_file.write(data)
                node_config_file.close()
            except Exception as err:
                print(f"[ERROR] Unable to compute node config for node {node+1}")
                print(str(err))
                for node in range(self.max_node_number):
                    self._remove_config_files(node)
                status= False
                pass
        print(info)
        return status

    def _remove_config_files(self, node):
        try:
            configFile= str(Path(__file__).parent.resolve())
            configFile+= f"/../scenarios/{self.scenario_name}/config/N{node+1}_node_config.h"
            os.remove(configFile)
        except:
            pass

    def _get_scenario_name(self, script_file):
        parent_path= Path(script_file).parent.absolute()
        return os.path.basename(os.path.normpath(parent_path))
