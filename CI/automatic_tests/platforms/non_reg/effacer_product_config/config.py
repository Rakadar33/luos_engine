# coding:utf-8
import os
import sys
from pathlib import Path
import time


# A ENLEVER
'''
Board_1,
Board_2,
Board_3,
Board_4,
Board_5,
Board_1, Board_2,
Board_1, Board_3,
Board_1, Board_4,
Board_1, Board_5,
Board_2, Board_3,
Board_2, Board_4,
Board_2, Board_5,
Board_3, Board_4,
Board_3, Board_5,
Board_4, Board_5,
Board_1, Board_2, Board_3
Board_1, Board_2, Board_4
Board_1, Board_2, Board_5
Board_1, Board_3, Board_4
Board_1, Board_3, Board_5
Board_1, Board_4, Board_5
Board_2, Board_3, Board_4
Board_2, Board_3, Board_5
Board_2, Board_4, Board_4
Board_3, Board_4, Board_5
Board_1, Board_2, Board_3, Board_4
Board_1, Board_2, Board_3, Board_5
Board_1, Board_2, Board_4, Board_5
Board_1, Board_3, Board_4, Board_5
Board_2, Board_3, Board_4, Board_5
Board_1, Board_2, Board_3, Board_4, Board_5
'''

Board_1= 1
Board_2= 2
Board_3= 3
Board_4= 4
Board_5= 5

networkConfig={}
networkConfig["N2"]=             {"num": 1,  "network": [Board_1],                                     "node_number": 1}
networkConfig["N3"]=             {"num": 3,  "network": [Board_3],                                     "node_number": 1}
networkConfig["N4"]=             {"num": 4,  "network": [Board_4],                                     "node_number": 1}
networkConfig["N5"]=             {"num": 5,  "network": [Board_5],                                     "node_number": 1}
networkConfig["N1_N2"]=          {"num": 6,  "network": [Board_1, Board_2],                            "node_number": 2}
networkConfig["N1_N3"]=          {"num": 7,  "network": [Board_1, Board_3],                            "node_number": 2}
networkConfig["N1_N4"]=          {"num": 8,  "network": [Board_1, Board_4],                            "node_number": 2}
networkConfig["N1_N5"]=          {"num": 9,  "network": [Board_1, Board_5],                            "node_number": 2}
networkConfig["N2_N3"]=          {"num": 10, "network": [Board_2, Board_3],                            "node_number": 2}
networkConfig["N2_N4"]=          {"num": 11, "network": [Board_2, Board_4],                            "node_number": 2}
networkConfig["N2_N5"]=          {"num": 12, "network": [Board_2, Board_5],                            "node_number": 2}
networkConfig["N3_N4"]=          {"num": 13, "network": [Board_3, Board_4],                            "node_number": 2}
networkConfig["N3_N5"]=          {"num": 14, "network": [Board_3, Board_5],                            "node_number": 2}
networkConfig["N4_N5"]=          {"num": 15, "network": [Board_4, Board_5],                            "node_number": 2}
networkConfig["N1_N2_N3"]=       {"num": 16, "network": [Board_1, Board_2, Board_3],                   "node_number": 3}
networkConfig["N1_N2_N4"]=       {"num": 17, "network": [Board_1, Board_2, Board_4],                   "node_number": 3}
networkConfig["N1_N2_N5"]=       {"num": 18, "network": [Board_1, Board_2, Board_5],                   "node_number": 3}
networkConfig["N1_N3_N4"]=       {"num": 19, "network": [Board_1, Board_3, Board_4],                   "node_number": 3}
networkConfig["N1_N3_N5"]=       {"num": 20, "network": [Board_1, Board_3, Board_5],                   "node_number": 3}
networkConfig["N1_N4_N5"]=       {"num": 21, "network": [Board_1, Board_4, Board_5],                   "node_number": 3}
networkConfig["N2_N3_N4"]=       {"num": 22, "network": [Board_2, Board_3, Board_4],                   "node_number": 3}
networkConfig["N2_N3_N5"]=       {"num": 23, "network": [Board_2, Board_3, Board_5],                   "node_number": 3}
networkConfig["N2_N4_N5"]=       {"num": 24, "network": [Board_2, Board_4, Board_5],                   "node_number": 3}
networkConfig["N3_N4_N5"]=       {"num": 25, "network": [Board_3, Board_4, Board_5],                   "node_number": 3}
networkConfig["N1_N2_N3_N4"]=    {"num": 26, "network": [Board_1, Board_2, Board_3, Board_4],          "node_number": 4}
networkConfig["N1_N2_N3_N5"]=    {"num": 27, "network": [Board_1, Board_2, Board_3, Board_5],          "node_number": 4}
networkConfig["N1_N2_N4_N5"]=    {"num": 28, "network": [Board_1, Board_2, Board_4, Board_5],          "node_number": 4}
networkConfig["N1_N3_N4_N5"]=    {"num": 29, "network": [Board_1, Board_3, Board_4, Board_5],          "node_number": 4}
networkConfig["N2_N3_N4_N5"]=    {"num": 30, "network": [Board_2, Board_3, Board_4, Board_5],          "node_number": 4}
networkConfig["N1_N2_N3_N4_N5"]= {"num": 31, "network": [Board_1, Board_2, Board_3, Board_4, Board_5], "node_number": 5}


class NetworkConfig:
    def __init__(self, scenario, conf):
        self.scenario_name= scenario
        #self.config= networkConfig.get(network)
        self.config= networkConfig[conf]
        self.max_node_number= 5
        self.config.get("POWER")
    def nodeConfig_generation(self):
        status= True
        for node in range(self.max_node_number):
            try:
                # Delete previous node_config files
                os.remove(f"../scenarios/{self.scenario_name}/config/N{node+1}_node_config.h")
            except:
                pass

        '''
        try:
        except:
            print("[ERROR] node config generation has failed")
            time.sleep(0.1)
            status= False
            pass
        return status
        '''


        for node in range(self.max_node_number):
            source= f"{Path( __file__ ).parent.absolute()}/template_N{node+1}_node_config.h"
            destination= f"{Path( __file__ ).parent.absolute()}/../scenarios/{self.scenario_name}/config/N{node+1}_node_config.h"
            pattern= "//#define PTP_CONFIG"
            new_config = f"//#define {}"

            try:
                # Compute node_config PTPs
                template_file = open(source, 'r')
                data = template_file.read()
                data = data.replace(pattern, new_config) 
                template_file.close()
                # Create node_config.h
                node_config_file = open(destination, 'x')
                node_config_file.write(data)
                node_config_file.close()
            except:
                print(f"[ERROR] Unable to compute node config for node {node+1}")
                pass

#------------
# test class
#------------
conf= NetworkConfig("000_template", "N1")
result= conf.nodeConfig_generation()
print(f"Result : {result}")
time.sleep(0.1)
assert(result)

# --------------
# OLD CODE
# --------------
"""
def find_version(version_file):
    is_version= False
    with open(version_file) as file:
        while 1:
            try:
                data = file.readline()
                version= "\"version\":"
                if version in data:
                    time.sleep(0.1)
                    version= data.split("\"")[3].split(".")
                    version_maj, version_min, version_patch= version
                    is_version= True
                    break
                elif len(data) == 0:
                    break
            except:
                print("\nError while searching version in file {version_file}\n")
                time.sleep(0.1)
                sys.exit()
    if not is_version:
        print(f"\nVersion number not found in {version_file}\n")        
        time.sleep(0.1)
        sys.exit()
    return version_maj, version_min, version_patch

def compute_version(rev, version_maj, version_min, version_patch):
    if rev == "MAJOR":
        version_maj = str(int(version_maj) + 1)
        version_min = "0"
        version_patch = "0"
    elif rev == "MINOR":
        version_min = str(int(version_min) + 1)
        version_patch = "0"
    elif rev == "PATCH":
        version_patch = str(int(version_patch) + 1)
    else:
        assert(rev == None)        
    return version_maj, version_min, version_patch


def replace(filePath, pattern, subs):
    with open(filePath, "r") as f:
        data = f.readlines()

    for index, line in enumerate(data):
        if pattern in line:
            data[index] = subs+"\n"

    with open(filePath, "w") as f:

        f.writelines(data)

def check(filePath, pattern):
    with open(filePath, "r") as f:
        data = f.readlines()

    for index, line in enumerate(data):
        if pattern in line:
            return True
    
    filePath= filePath.replace("library.json", "")
    print(f"[Warning] Unable to find \"{pattern}\" in \"{filePath}\"")
    time.sleep(0.1)
    return False

def version_assert(status, file):
    if not status:
        print(f"\n*** ERROR***\n\t Version control for file {file}")
        sys.exit(1)
   
if __name__ == '__main__':

    # Arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str)
    parser.add_argument('--path', type=str)    
    args = parser.parse_args()

    possible_values=("MAJOR", "MINOR", "PATCH")
    if (not args.type in possible_values):
        print(f"\npython create_version.py --path LUOS_ENGINE_PATH --type [MAJOR][MINOR][PATCH]\n")
        sys.exit()

    basePath = args.path
    if (basePath == None):
        print(f"\nUSAGE:\n\tpython create_version.py --path LUOS_ENGINE_PATH --type [MAJOR][MINOR][PATCH]\n")
        sys.exit()        


    #--------------------------------------
    # Compute versions
    #--------------------------------------
    
    # Find Luos_engine version
    major, minor, patch= find_version(f"{basePath}\\library.json")
    print(f"[   -OLD-   ] Luos engine version : {major}.{minor}.{patch}")
    major, minor, patch= compute_version(args.type, major, minor, patch)
    new_version= f"{major}.{minor}.{patch}"
    print(f"[ -UPDATED- ] Luos engine version : {new_version}\n")

    # Find Pipe version
    file_pipe= f"{basePath}\\tool_services\\pipe\\library.json"
    major_pipe, minor_pipe, patch_pipe= find_version(file_pipe)
    print(f"[   -OLD-   ] PIPE version : {major_pipe}.{minor_pipe}.{patch_pipe}")
    major_pipe, minor_pipe, patch_pipe= compute_version(args.type, major_pipe, minor_pipe, patch_pipe)
    new_version_pipe= f"{major_pipe}.{minor_pipe}.{patch_pipe}"
    print(f"[ -UPDATED- ] PIPE version : {new_version_pipe}\n")

    # Find Gate version
    file_gate= f"{basePath}\\tool_services\\gate\\library.json"
    major_gate, minor_gate, patch_gate= find_version(file_gate)
    print(f"[   -OLD-   ] GATE version : {major_gate}.{minor_gate}.{patch_gate}")
    major_gate, minor_gate, patch_gate= compute_version(args.type, major_gate, minor_gate, patch_gate)
    new_version_gate= f"{major_gate}.{minor_gate}.{patch_gate}"
    print(f"[ -UPDATED- ] GATE version : {new_version_gate}\n")

    # Find Inspector version
    file_insp= f"{basePath}\\tool_services\\inspector\\library.json"
    major_inspector, minor_inspector, patch_inspector= find_version(file_insp)
    print(f"[   -OLD-   ] INSPECTOR version : {major_inspector}.{minor_inspector}.{patch_inspector}")
    major_inspector, minor_inspector, patch_inspector= compute_version(args.type, major_inspector, minor_inspector, patch_inspector)
    new_version_inspector= f"{major_inspector}.{minor_inspector}.{patch_inspector}"
    print(f"[ -UPDATED- ] INSPECTOR version : {new_version_inspector}\n")

    #--------------------------------------
    # Update versions numbers
    #--------------------------------------

    # Update : README.md
    file= f"{basePath}\\README.md"
    pattern= "Version:" 
    sub= f"{pattern} {new_version}"
    replace(file, pattern, sub)
    version_assert(check(file, sub), file)

    # Update : Luos version
    file= f"{basePath}\\engine\\core\\src\\luos_engine.c"
    pattern= "revision_t luos_version = " 
    sub= f"{pattern}" + "{" + f".major = {major}, .minor = {minor}, .build = {patch}" +"};"
    replace(file, pattern, sub)
    version_assert(check(file, sub), file)

    file= f"{basePath}\\library.json"
    pattern= "\"version\":"
    sub= f"    {pattern}" +  f"\"{major}.{minor}.{patch}\","
    replace(file, pattern, sub)
    version_assert(check(file, sub), file)

    # Update : library.json
    library= "library.json"
    pattern= "luos_engine\":"
    sub= f"\t\"luos/{pattern} \"^{major}.{minor}.{patch}\"" 

    # search all "library.json" files
    for root, dirs, files in os.walk(basePath):
        for file in files:
            if (file == library) and (not '.pio' in root):
                current_file = os.path.join(root,file)
                if check(current_file, pattern):
                    replace(current_file, pattern, sub)
                    version_assert(check(current_file, sub), file)

    # Update : Pipe
    pattern= "\"version\":"
    sub= f"    {pattern} \"{major_pipe}.{minor_pipe}.{patch_pipe}\","
    replace(file_pipe, pattern, sub)
    version_assert(check(file_pipe, sub), file_pipe)

    # Update : Gate
    pattern= "\"version\":"
    sub= f"    {pattern} \"{major_gate}.{minor_gate}.{patch_gate}\","
    replace(file_gate, pattern, sub)
    version_assert(check(file_gate, sub), file_gate)

    # Update : Inspector
    pattern= "\"version\":"
    sub= f"    {pattern} \"{major_inspector}.{minor_inspector}.{patch_inspector}\","
    replace(file_insp, pattern, sub)
    version_assert(check(file_insp, sub), file_insp)

    # Update : platformio.ini
    pf_IO= "platformio.ini"
    pattern= "luos_engine@"
    sub= f"luos_engine@^{major}.{minor}.{patch}"

    # search all "platformio.ini" files
    for root, dirs, files in os.walk(basePath):
        for file in files:
            if file == pf_IO:
                current_file = os.path.join(root,file)
                if check(current_file, pattern):
                    replace(current_file, pattern, sub)
                    version_assert(check(current_file, sub), file)

    print("\n" + 70*"*")
    print("[Warning] Don't forget to update version manually for projects :")
    print("\t\t* \"Bootloader\"")
    print("\t\t* \"Example libs\"")
    print(70*"*")
    print(f"[OK] New Luos Engine versions {new_version} is generated")
    print(70*"*" + "\n")

"""