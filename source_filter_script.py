import uuid
import sys
import subprocess
import platform as pf
from os import system, listdir, path, scandir, getcwd
import click
import json
import requests

from os.path import join, realpath
Import("env")

telemetry = True
luos_telemetry = {"telemetry_type": "luos_engine_build",
                  "mac": hex(uuid.getnode()),
                  "system": sys.platform,
                  "unix_time": env.get("UNIX_TIME"),
                  "platform": env.get("PIOPLATFORM"),
                  "mcu": env.get("BOARD_MCU"),
                  "f_cpu": env.get("BOARD_F_CPU")}

try:
    luos_telemetry["framework"] = env.get("PIOFRAMEWORK")[0]
except:
    pass

# Check if this script have been already executed during this compilation
visited_key = "__LUOS_CORE_SCRIPT_CALLED"
global_env = DefaultEnvironment()

if not visited_key in global_env:
    click.secho("")
    click.secho("Luos engine build configuration:", underline=True)
    # install pyluos
    try:
        import pyluos
        env.Execute("$PYTHONEXE -m pip install pyluos --upgrade --quiet")
    except ImportError:  # module doesn't exist, deal with it.
        env.Execute("$PYTHONEXE -m pip install pyluos")
        pass
    try:
        from pyluos import version
        click.secho("\t* Pyluos revision " +
                    str(version.version) + " ready.", fg="green")
        luos_telemetry["pyluos_rev"] = str(version.version)
    except ImportError:  # module doesn't exist, deal with it.
        click.secho(
            "\t* Pyluos install failed. Platformio will be unable to use bootloader flash feature.", fg="red")
        luos_telemetry["pyluos_rev"] = "none"

sources = ["+<*.c>",
           "+<../../../network/robus/src/*.c>",
           "+<../../profiles/state/*.c>",
           "+<../../profiles/motor/*.c>",
           "+<../../profiles/servo_motor/*.c>",
           "+<../../profiles/voltage/*.c>",
           "+<../../bootloader/*.c>"]

# private library flags
find_HAL = False
for item in env.get("CPPDEFINES", []):
    if isinstance(item, tuple) and item[0] == "LUOSHAL":
        find_HAL = True
        if (path.exists("network/robus/HAL/" + item[1]) and path.exists("engine/HAL/" + item[1])):
            if not visited_key in global_env:
                click.secho(
                    "\t* %s HAL selected for Luos and Robus." % item[1], fg="green")
                luos_telemetry["luos_hal"] = item[1]
        else:
            if not visited_key in global_env:
                click.secho("\t* %s HAL not found" % item[1], fg="red")
                luos_telemetry["luos_hal"] = "invalid" + str(item[1])
        env.Append(CPPPATH=[realpath("network/robus/HAL/" + item[1])])
        env.Append(CPPPATH=[realpath("engine/HAL/" + item[1])])
        env.Replace(SRC_FILTER=sources)
        env.Append(
            SRC_FILTER=["+<../../../network/robus/HAL/%s/*.c>" % item[1]])
        env.Append(SRC_FILTER=["+<../../HAL/%s/*.c>" % item[1]])
    if (item == 'NOTELEMETRY'):
        telemetry = False


if (telemetry == True):
    click.secho("\t* Telemetry enabled.", fg="green")
    try:
        requests.post("https://monorepo-services.vercel.app/api/telemetry",
                      data=luos_telemetry)
    except:
        click.secho("Telemetry request failed.", fg="red")
else:
    click.secho("\t* Telemetry disabled, please consider enabling it by removing the 'NOTELEMETRY' flag to help Luos_engine improve.", fg="red")
click.secho("")

# native unit testing
find_MOCK_HAL = False
for item in env.ParseFlags(env['BUILD_FLAGS'])["CPPDEFINES"]:
    if (item == 'UNIT_TEST'):
        click.secho("Native unit testing:", underline=True)
        current_os = pf.system()
        if find_MOCK_HAL == False:
            click.secho(
                "\t* Mock HAL for %s is selected for Luos and Robus." % current_os, fg="green")
        find_MOCK_HAL = True
        find_HAL = True
        env.Replace(SRC_FILTER=sources)
        env.Append(SRC_FILTER=["-<test/>"])
        env.Append(SRC_FILTER=["+<../../../test/_resources/*>"])

        for resources in scandir(getcwd() + "/test/_resources"):
            if resources.is_dir():
                env.Append(CPPPATH=[(resources.path)])

        if (current_os == 'Linux') or (current_os == 'Darwin'):
            env.Append(LINKFLAGS=["-m32"])
        elif current_os == 'Windows':
            env.Append(LINKFLAGS=["-lgcov"])
            env.Append(LINKFLAGS=["--coverage"])
            env.Append(LINKFLAGS=["-fprofile-arcs"])

            def generateCoverageInfo(source, target, env):
                for file in os.listdir("test"):
                    env.Execute(".pio/build/native/program test/"+file)
                env.Execute("lcov -d .pio/build/native/ -c -o lcov.info")
                env.Execute(
                    "lcov --remove lcov.info '*/tool-unity/*' '*/test/*' -o filtered_lcov.info")
                env.Execute(
                    "genhtml -o cov/ --demangle-cpp filtered_lcov.info")

            # Generate code coverage when testing workflow is ended
            # CODE COVERAGE WILL BE ADDED SOON
            # env.AddPostAction(".pio/build/native/program", generateCoverageInfo)
        else:
            click.echo("Unit tests are not supported on your os ", current_os)
        break
    else:
        break

if not visited_key in global_env:
    if (find_HAL == False):
        click.echo(click.style("\t* No HAL selected. Please add a ", fg="red") + click.style(
            "-DLUOSHAL", fg="red", bold=True) + click.style(" compilation flag", fg="red"))

global_env[visited_key] = True
