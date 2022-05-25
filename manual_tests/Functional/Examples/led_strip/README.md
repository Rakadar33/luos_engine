# Test Module Description : 

## Module tested
**name**: Led strip example  
**version**: NA  
**sources**: [led_strip_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Led_strip)  

## Goal

This test aims to validate the led strip example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom), and a [led_strip](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Led_strip). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [led_strip notebook](./rainbow_led_strip.ipynb)

#### Step 1 
Launch the first section, make sure that you give the right dimensions of your led strip, you should see your network appear
#### Step 2
Launch the second section, you should see the led_strip changing colors as a rainbow