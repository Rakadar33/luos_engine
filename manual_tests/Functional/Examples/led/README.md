# Test Module Description : 

## Module tested
**name**: Led example  
**version**: NA  
**sources**: [led_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Led)  

## Goal

This test aims to validate the led example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom), and a [led](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Led). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [led notebook](./led_test.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
Launch the second section, you should see the led changing from red to green and blue
#### Step 3
Launch the second section and you should your led lighting like a disco ball!