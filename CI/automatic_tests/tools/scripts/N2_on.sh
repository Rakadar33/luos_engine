#!/bin/bash

BASEDIR=$(dirname "$0")
AUTO_TEST_PATH=${BASEDIR}"/../../"
export PYTHONPATH=$AUTO_TEST_PATH:$PYTHONPATH

source usbhub/bin/activate
python3 $BASEDIR/capable-robot-driver.py  --port 2 --power ON
deactivate

