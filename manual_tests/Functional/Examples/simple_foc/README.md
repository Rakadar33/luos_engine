# Test Module Description :

## Module tested

**name**: Simple FOC bldc & stepper motor examples

## Goal

This test aims to validate the simple foc stepper and bldc examples

## Setup

this tests uses arduino boards connected to bldc and stepper drivers.

## Procedure

For the BLDC, open [bldc_motor notebook](./simple_foc_bldc.ipynb).

For the stepper, open [stepper_motor notebook](./simple_foc_stepper.ipynb).

#### Step 1

Launch the first section, your motor should turn until it reaches the 270°
position.

#### Step 2

Launch the section, your motor should return to the 0° position.

#### Step 3

Launch the section, the motor should turn at a fixed angular speed.

#### Step 4

The four next sections allows to test the trajectory mode. You can generate two
trajectory:

- the first goes from 0° to 360°
- the second goes from 360° to 0°

The following instruction send the trajectory to the motor which immediatly
start moving:

> dev.Stepper_FOC.target_rot_position = traj
