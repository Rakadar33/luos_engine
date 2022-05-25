# Test Module Description : 

## Module tested
**name**: Light sensor example  
**version**: NA  
**sources**: [light_sensor_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Light_sensor)  

## Goal

This test aims to validate the light sensor example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom), and a [light_sensor](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Light_sensor). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [light_sensor notebook](./light_sensor.ipynb)

#### Step 1 
Launch the first section, make sure that you give the right dimensions of your light sensor, you should see your network appear
#### Step 2
Launch the second section, you should see the values captured by the sensor depending on the light