#!/bin/bash

# For debug
# set -x

# Safety measures
# set -o errexit  # Leave immediately if a command returns an error
set -o nounset  # Leave immediately if an unitialized value is used
set -o pipefail # Leave immediately if a command fails in a pipe

#Paramater
LUOS_BRANCH=${1}
HAL_BRANCH=${2}

# Check parameters
[[ -z $LUOS_BRANCH ]]  && (echo "usage: $0 <LUOS_BRANCH> <HAL_BRANCH>"; exit 1)
[[ -z $HAL_BRANCH ]]   && (echo "usage: $0 <LUOS_BRANCH> <HAL_BRANCH>"; exit 1)

#Constants
export PATH="$PATH:$PWD/../.platformio/packages/toolchain-gccarmnoneeabi/bin/"
SCRIPT_TIMEOUT=150 #seconds
WORKSPACE=$(pwd)/../PF/Quality_assurance/Platforms/Delivery_Platform
LOGFILENAME=test_result.log

lock=$(ps -aux | grep 'stress-test.sh' | grep 'www-data' | wc -l)
if (($lock != 5))
then
    # Someone is already using this script
    echo "A test is already launched on the platform, please try again in a few minutes..."
    exit 0
else
    # No script is in progress :  launch platform script (with timeout after SCRIPT_TIMEOUT seconds)
    current_date=$(date)    
    log_date_filename=$(date '+%Y_%m_%d__%Hh%M_%S_')$LOGFILENAME

    echo '-----------------------------------------------------------------'
    echo "Clone Luos    repo on branch "$LUOS_BRANCH
    echo "Clone LuosHAL repo on branch "$HAL_BRANCH    
    echo '-----------------------------------------------------------------'
	cd $(pwd)/../PF/Workspace
	rm -Rf ./Luos
	rm -Rf ./LuosHAL

	#Clone Luos git repo	
	git clone https://github.com/Luos-io/Luos.git
	cd ./Luos
    git checkout $LUOS_BRANCH
    if (($? != 0))
    then
      echo "Unknown branch LUOS "$LUOS_BRANCH
      exit 1
    fi
	git branch        

	#Clone LuosHAL git repo
	cd ..
	git clone https://github.com/Luos-io/LuosHAL.git
	cd ./LuosHAL
	git checkout $HAL_BRANCH
    if (($? != 0))
    then
      echo "Unknown branch LUOS "$HAL_BRANCH
      exit 1
    fi
	git branch

    echo '-----------------------------------------------------------------'
    echo "Stress test launched on $current_date"
    echo '-----------------------------------------------------------------'
    usb=$(echo /dev/ttyU*  | awk '{ print $NF }')

    if [[ $usb =~ ['*'] ]];
    then
        echo "No Gate found, test is cancelled"
        exit 1
    else
    	echo "Gate found on USB: "$usb
    fi

	rm $WORKSPACE/Results/$LOGFILENAME;    
    timeout --preserve-status $SCRIPT_TIMEOUT python3 $WORKSPACE/Tests/Delivery_Platform.py --serial-port $usb
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
fi
