#!/bin/bash
# Safety measures
set -o errexit  # Leave immediately if a command returns an error
set -o nounset  # Leave immediately if an unitialized value is used
set -o pipefail # Leave immediately if a command fails in a pipe

SCRIPT_TIMEOUT=150 #seconds
echo $PATH
#export PATH="$PATH:/var/www/.platformio/packages/toolchain-gccarmnoneeabi/bin/"
export PATH="$PATH:$PWD/../.platformio/packages/toolchain-gccarmnoneeabi/bin/"
echo $PATH
cd ../PF/Quality_assurance/Platforms/Delivery_Platform/Projects/NUCLEO_L4/


platformio run -t clean 2>&1
platformio run  2>&1
platformio run -v -t upload 2>&1
echo 'L4 is Uploaded'
exit 0
