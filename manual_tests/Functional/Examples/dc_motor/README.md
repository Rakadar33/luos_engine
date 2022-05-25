# Test Module Description : 

## Module tested
**name**: dc motor example
**version**: NA  
**sources**: [dc_motor_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Dc_motor)

## Goal

This test aims to validate the dc example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom) and a [dc_motor](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Dc_motor). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, you have a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom), a [dc_motor](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Dc_motor) with 2 dc motor and wired, a [jack power input](https://github.com/Luos-io/Examples/tree/master/Hardware/wiring_and_power/Jack_power_input). you must have a power supply link to the jack power input board to 5V 2A. open the [dc_motor notebook](./dc_motor.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
launch the second section.

- motor 1 should turn counter clock wise at a ratio of 70% of VCC during 3 sec
- motor 1 should turn clock wise at a ratio of 25% of VCC during 3 sec.
- motor 1 should turn stop.
- motor 2 should turn counter clock wise at a ratio of 50% of VCC during 3 sec.
- motor 2 should turn clock wise at a ratio of 25% of VCC during 3 sec.
- motor 2 should turn stop.

see the [salae trace](./PWM_command.png) to check pwm command. see the [salae trace motor 1](./PWM_dc1.png) and see the [salae trace motor 2](./PWM_dc2.png) for pwm ratio
