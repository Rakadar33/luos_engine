# Test Module Description : 

## Module tested
**name**: Button example  
**version**: NA  
**sources**: [button_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Button)  

## Goal

This test aims to validate the button example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom) and a [button](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Button). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [button notebook](./button.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
Release the button and launch the second section, you should see **False** appear.
#### Step 3
Press the button and relaunch the second section, you should see **True** appear.