# Test Module Description : 

## Module tested
**name**: servo
**version**: NA  
**sources**: [dc_motor_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Servo)

## Goal

This test aims to validate the dc example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom) and a [Servo](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Servo). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, you have a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom), a [Servo](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Servo) with 1 servo and wired, a [jack power input](https://github.com/Luos-io/Examples/tree/master/Hardware/wiring_and_power/Jack_power_input). you must have a power supply link to the jack power input board to 12V 2A. open the [Servo notebook](./Servo.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
launch the second section.

- Servo 1 should go to position 90°. change to Servo 2
- Servo 2 should go to position 180°.change to Servo 3
- Servo 3 should go to position 45°.change to Servo 4
- Servo 4 should go to position 120°.

see the [salae trace](./servo_pwm.png) to check pwm command.
