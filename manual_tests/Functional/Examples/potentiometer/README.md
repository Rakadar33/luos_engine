# Test Module Description : 

## Module tested
**name**: Potentiometer example  
**version**: NA  
**sources**: [potentiometer_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Potentiometer)  

## Goal

This test aims to validate the potentiometer example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom), and a [potentiometer](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Potentiometer). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [potentiometer notebook](./potentiometer_test.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
Launch the second section, you should see the printed values changing while you are turning your potentiometer.