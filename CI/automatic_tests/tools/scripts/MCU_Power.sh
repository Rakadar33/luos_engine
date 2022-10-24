#!/bin/bash
clear;python3 power.py  --port 1 --power ON;sleep 1;python3 power.py  --port 2 --power ON;sleep 1;python3 power.py  --port 3 --power ON;sleep 1;python3 power.py  --port 4 --power ON;sleep 1;python3 power.py  --port 1 --power OFF;sleep 1;python3 power.py  --port 2 --power OFF;sleep 1;python3 power.py  --port 3 --power OFF;sleep 1;python3 power.py  --port 4 --power OFF
