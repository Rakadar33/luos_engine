# Test Module Description : 

## Module tested
**name**: power_switch example  
**version**: NA  
**sources**: [power_switch_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Power_switch)  

## Goal

This test aims to validate the power_switch example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom) and a [power_switch](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Power_switch). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [power_switch notebook](./power_switch.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
Launch the second section, you should see the switch **closed**.
#### Step 3
Launch the third section, you should see the switch **opened**.