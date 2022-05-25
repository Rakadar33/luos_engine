# Test Module Description : 

## Module tested
**name**: Distance example
**version**: NA  
**sources**: [Distance_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Distance)

## Goal

This test aims to validate the Distance example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom) and a [Distance](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Distance). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [Distance notebook](./Distance.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
Put an obstacle at different distance you should see the distance between the sensor and the obstacle in meters. the value is update every 0.5s
