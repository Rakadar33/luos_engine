#!/bin/bash

#Paramater
id=${1}

#constants
SCRIPT_TIMEOUT=5

[[ -z $id ]]  && (echo "usage: $0 <USB NUMBER>"; exit 1)

##usb=$(echo /dev/ttyU*  | awk '{ print $NF }')
#usb=$(echo /dev/ttyUSB$id  | awk '{ print $NF }')
#if [[ $usb =~ ['*'] ]]; then
#    #echo "No Gate found, test is cancelled"
#    exit 2
#fi

#timeout --preserve-status $SCRIPT_TIMEOUT pyluos-bootloader detect /dev/ttyUSB$id
timeout --preserve-status $SCRIPT_TIMEOUT res=pyluos-bootloader detect /dev/ttyUSB$id
if (($? == 0)); then
    exit 0
else
    echo "$0 error"
    exit 3
fi
