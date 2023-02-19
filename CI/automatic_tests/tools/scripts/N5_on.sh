#!/bin/bash

CURRENT_PATH=$(pwd)
AUTO_TEST_PATH=${CURRENT_PATH}"/../../"
export PYTHONPATH=$AUTO_TEST_PATH:$PYTHONPATH
clear
python3 N5_power_on.py
