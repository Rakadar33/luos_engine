#!/bin/bash

# For debug
# set -x

# Safety measures
# set -o errexit  # Leave immediately if a command returns an error
######set -o nounset  # Leave immediately if an unitialized value is used
######set -o pipefail # Leave immediately if a command fails in a pipe

#Paramater
LUOS_BRANCH=main

#Constants
export PATH="$PATH:/root/.platformio/packages/toolchain-gccarmnoneeabi/bin/"
SCRIPT_TIMEOUT=20 #seconds
WORKSPACE=/qa/tests
LOGFILENAME=test_result.log

current_date=$(date)    
log_date_filename=$(date '+%Y_%m_%d__%Hh%M_%S_')$LOGFILENAME

echo "Get RTB - $current_date"
usb=$(echo /dev/ttyU*  | awk '{ print $NF }')

if [[ $usb =~ ['*'] ]];
then
    echo "No Gate found, test is cancelled"
    exit 1
else
	echo "Gate found on USB: "$usb
fi

#rm $WORKSPACE/Results/$LOGFILENAME;    
pwd
cat ./tests/Tests/test_detect.py
pwd
exit 0
#python3 test_detect.py
timeout --preserve-status $SCRIPT_TIMEOUT pwd
if (($? == 0))
then
    cd $WORKSPACE/Results/
    cp $LOGFILENAME $log_date_filename   
    echo '-----------------------------------------------------------------'
    echo "End of script : OK"
    echo '-----------------------------------------------------------------'
    exit 0
else
    cd $WORKSPACE/Results/
    cp $LOGFILENAME $log_date_filename   
    echo '-----------------------------------------------------------------'
    echo "End of script : KO"
    echo "    - Either an ERROR occured"
       echo "    - Or a TIMEOUT occured after $SCRIPT_TIMEOUT seconds"
    echo '-----------------------------------------------------------------'	
      	echo ' '	
   	echo ' '	

   	ko_nb=$(cat     $log_date_filename | grep -i KO    | wc -l)
   	error_nb=$(cat  $log_date_filename | grep -i ERROR | wc -l)

       if (($error_nb > 0))
       then
   		echo 'Errors :'	
        echo '----------------'	
   	    cat  $log_date_filename | grep -i ERROR
       fi
       if (($ko_nb > 0))
       then
   		echo 'Steps KO :'	
        echo '----------------'	
   	    cat  $log_date_filename | grep -i KO
       fi        
	echo ' '        
    exit 1
fi
