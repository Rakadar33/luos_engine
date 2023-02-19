#!/bin/bash

CURRENT_PATH=$(pwd)
AUTO_TEST_PATH=${CURRENT_PATH}"/../../"
export PYTHONPATH=$AUTO_TEST_PATH:$PYTHONPATH
clear
python3 capable-robot-driver.py  --port 2 --power OFF
