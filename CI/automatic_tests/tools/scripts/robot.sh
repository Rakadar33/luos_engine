#!/bin/bash

export PYTHONPATH=/home/luos_adm/Luos_tests/Docker/Quality_assurance/CI/automatic_tests:$PYTHONPATH
cd /home/luos_adm/Luos_tests/Docker/Quality_assurance/CI/automatic_tests/platforms/non_reg/scenarios/001_get_started
python3 scenario.py  --upload ON
python3 mail.py
#python3 scenario.py
