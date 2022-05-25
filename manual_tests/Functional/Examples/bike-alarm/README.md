# Test Module Description : 

## Module tested
**name**: Bike Alarm example  
**version**: NA  
**sources**: [bike_alarm_sources](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Bike_alarm)  

## Goal

This test aims to validate the bike alarm example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom), a led used as [alarm_controller](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Bike_alarm/Alarm_controller), a button used as [start_controller](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Bike_alarm/Start_controller) and an [imu](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Imu). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [bike alarm notebook](./Connected_bike.ipynb)

Launch the first section, you should see your network appear
you can press the button in order to lock and unlock th bike. By default the bike is locked and the alarm is playing
#### Step 2
Launch the second section and you will unlock the bike by using start_controller
#### Step 3
Launch the third section and you will relock the bike by triggering alarm_controller
#### Step 4
Launch the fourth section and you will unlock the bike by triggering alarm_controller
#### Step 5
Launch the fifth section and you should see a stable color to your led
#### Step 6
Launch the sixth section to relock the bike and activate the alarm