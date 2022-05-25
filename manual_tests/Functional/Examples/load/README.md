# Test Module Description : 

## Module tested
**name**: Load example
**version**: NA  
**sources**: [Load_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Load)

## Goal

This test aims to validate the Load example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom) and a [Load](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Load). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [Load notebook](./load.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
Put an weight of 100g on the load sensor you should see the equivalent weight in mN. the value is update every 0.5s
