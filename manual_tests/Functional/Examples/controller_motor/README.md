# Test Module Description : 

## Module tested
**name**: controller_motor example  
**version**: NA  
**sources**: [controller_motor_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Controller_motor)  

## Goal

This test aims to validate the controller_motor example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom) and a [stepper](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Controller_motor). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [controller_motor notebook](./controller_motor.ipynb)

#### Step 1 
Launch the first notebook section, you should see the following message:

Sending detection signal.
Waiting for routing table...
Device setup.
-------------------------------------------------
Type                Alias               ID   
-------------------------------------------------
Gate                gate                1    
Pipe                Pipe                2    
ServoMotor          servo_motor         3  

#### Step 2
Launch the second section, you should see the following message:

> Connection OK

#### Step 3
Launch the third section, the motor should rotate 360° in one way then 360) in the other.

#### Step 4
Launch the fourth section, the motor should follow the displayed trajectory.