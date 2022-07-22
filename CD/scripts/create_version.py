# coding:utf-8
import os
import sys
import shutil
import subprocess
import argparse
import time
from termcolor import colored

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
                print(colored("\nError while searching version in file {version_file}\n","red"))
                time.sleep(0.1)
                sys.exit()
    if not is_version:
        print(colored(f"\nVersion number not found in {version_file}\n","red"))
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
    status = False
    comma = False
    with open(filePath, "r") as f:
        data = f.readlines()

    for index, line in enumerate(data):
        if pattern in line:
            if "," in line:
                comma = True #add a comma (",") at end of line if needed
            status = True
            break
    if not status:
        filePath= filePath.replace("library.json", "")
        print(colored(f"[Warning] \"{pattern}\" not found in \"{filePath}\"","yellow"))
        time.sleep(0.1)
    return status, comma 

def version_assert(status, file):
    if not status:
        print(colored(f"\n*** ERROR***\n\t Version control for file {file}","red"))
        sys.exit(1)
   
if __name__ == '__main__':
    # Arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str)
    parser.add_argument('--path', type=str)    
    parser.add_argument('--dev', type=str)    
    args = parser.parse_args()

    possible_values=("MAJOR", "MINOR", "PATCH")
    if (not args.type in possible_values):
        print(colored(f"\npython create_version.py --path LUOS_ENGINE_PATH --type [MAJOR][MINOR][PATCH] --dev [ON][OFF]\n","magenta"))
        sys.exit()

    basePath = args.path
    if (basePath == None):
        print(colored("\nUSAGE:\n\tpython create_version.py --path LUOS_ENGINE_PATH --type [MAJOR][MINOR][PATCH] --dev [ON][OFF]\n","magenta"))
        sys.exit()        

    if args.dev == "ON":
        dev = True
    elif args.dev == "OFF":
        dev = False
    else:
        print(colored("\nUSAGE:\n\tpython create_version.py --path LUOS_ENGINE_PATH --type [MAJOR][MINOR][PATCH] --dev [ON][OFF]\n","magenta"))
        sys.exit()        

    #--------------------------------------
    # Compute versions
    #--------------------------------------
    # Find Luos_engine version
    old_major, old_minor, old_patch= find_version(f"{basePath}\\library.json")
    major, minor, patch= compute_version(args.type, old_major, old_minor, old_patch)
    new_version= f"{major}.{minor}.{patch}"

    print(colored("\n" + 40*"*", "blue"))
    print(colored(f"    Generate {args.type} version {new_version}","blue"))
    if dev:
        print(colored(f"DEV VERSION","yellow"))
    print(colored(40*"*" + "\n", "blue"))
    print(colored(f"[   -OLD-   ] Luos engine version : {old_major}.{old_minor}.{old_patch}", "cyan"))
    print(f"[ -UPDATED- ] Luos engine version : {new_version}\n")

    # Find Pipe version
    file_pipe= f"{basePath}\\tool_services\\pipe\\library.json"
    major_pipe, minor_pipe, patch_pipe= find_version(file_pipe)
    print(colored(f"[   -OLD-   ] PIPE version : {major_pipe}.{minor_pipe}.{patch_pipe}", "cyan"))
    major_pipe, minor_pipe, patch_pipe= compute_version(args.type, major_pipe, minor_pipe, patch_pipe)
    new_version_pipe= f"{major_pipe}.{minor_pipe}.{patch_pipe}"
    print(f"[ -UPDATED- ] PIPE version : {new_version_pipe}\n")

    # Find Gate version
    file_gate= f"{basePath}\\tool_services\\gate\\library.json"
    major_gate, minor_gate, patch_gate= find_version(file_gate)
    print(colored(f"[   -OLD-   ] GATE version : {major_gate}.{minor_gate}.{patch_gate}", "cyan"))
    major_gate, minor_gate, patch_gate= compute_version(args.type, major_gate, minor_gate, patch_gate)
    new_version_gate= f"{major_gate}.{minor_gate}.{patch_gate}"
    print(f"[ -UPDATED- ] GATE version : {new_version_gate}\n")

    # Find Inspector version
    file_insp= f"{basePath}\\tool_services\\inspector\\library.json"
    major_inspector, minor_inspector, patch_inspector= find_version(file_insp)
    print(colored(f"[   -OLD-   ] INSPECTOR version : {major_inspector}.{minor_inspector}.{patch_inspector}", "cyan"))
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
    status, _ = check(file, sub)
    version_assert(status, file)

    # Update : Luos version
    file= f"{basePath}\\engine\\core\\src\\luos_engine.c"
    pattern= "revision_t luos_version = " 
    sub= f"{pattern}" + "{" + f".major = {major}, .minor = {minor}, .build = {patch}" +"};"
    replace(file, pattern, sub)
    status, _ = check(file, sub)
    version_assert(status, file)

    file= f"{basePath}\\library.json"
    pattern= "\"version\":"
    sub= f"    {pattern}" +  f"\"{major}.{minor}.{patch}\","
    replace(file, pattern, sub)
    status, _ = check(file, sub)
    version_assert(status, file)

    # Update : library.json
    library= "library.json"
    pattern= "luos_engine\":"
    # search all "library.json" files
    for root, dirs, files in os.walk(basePath):
        for file in files:
            if (file == library) and (not '.pio' in root):
                current_file = os.path.join(root,file)
                status, comma = check(current_file, pattern)
                if dev:
                    sub= f"\t\"{pattern} \"^{major}.{minor}.{patch}\"" 
                else:
                    sub= f"\t\"luos/{pattern} \"^{major}.{minor}.{patch}\"" 
                if comma:
                    sub+= "," 
                if status:
                    replace(current_file, pattern, sub)
                    version_assert(check(current_file, sub), file)

    # Update : Pipe
    pattern= "\"version\":"
    sub= f"    {pattern} \"{major_pipe}.{minor_pipe}.{patch_pipe}\","
    replace(file_pipe, pattern, sub)
    status, _ = check(file_pipe, sub)
    version_assert(status, file_pipe)

    # Update : Gate
    pattern= "\"version\":"
    sub= f"    {pattern} \"{major_gate}.{minor_gate}.{patch_gate}\","
    replace(file_gate, pattern, sub)
    status, _ = check(file_gate, sub)
    version_assert(status, file_gate)

    # Update : Inspector
    pattern= "\"version\":"
    sub= f"    {pattern} \"{major_inspector}.{minor_inspector}.{patch_inspector}\","
    replace(file_insp, pattern, sub)
    status, _ = check(file_insp, sub)
    version_assert(status, file_insp)

    # Update : platformio.ini
    pf_IO= "platformio.ini"
    pattern= "luos_engine@"
    sub= f"    luos_engine@^{major}.{minor}.{patch}"
    # search all "platformio.ini" files
    for root, dirs, files in os.walk(basePath):
        for file in files:
            if file == pf_IO:
                current_file = os.path.join(root,file)
                status, _ = check(current_file, pattern)
                if status:
                    replace(current_file, pattern, sub)
                    version_assert(check(current_file, sub), file)

    print(colored("\n" + 70*"*", "blue"))
    print(colored("[Warning] Don't forget to update version manually for projects :","blue"))
    print(colored("\t\t* \"Bootloader\"","blue"))
    print(colored("\t\t* \"Example libs\"","blue"))
    print(colored(70*"*", "blue"))
    print(colored(f"\n\t[OK] New Luos Engine versions {new_version} is generated\n","green"))
