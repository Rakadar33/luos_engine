# Test Module Description : 

## Module tested
**name**: gpio example  
**version**: NA  
**sources**: [gpio_source](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gpio)  

## Goal

This test aims to validate the gpio example packed in [examples](https://github.com/Luos-io/Examples).

## Setup

This test uses a [gate](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gate_SerialCom) and a [gpio](https://github.com/Luos-io/Examples/tree/master/Projects/l0/Gpio). Each one is flashed in a [l0 board](https://github.com/Luos-io/Examples/tree/master/Hardware/l0), they are linked by the luos network. The gate is connected to a PC through a **USB** cable.

## Procedure

Once the hardware is flashed and ready, open the [gpio notebook](./gpio.ipynb)

#### Step 1 
Launch the first section, you should see your network appear
#### Step 2
1. Connect with a cable P2 pin to P1 pin.
2. Launch the second section

You should see the following result:
| Pin         | result         |
|-------------|----------------|
| P1 voltage: | v > 3.0v       | 
| P7 voltage: | 1.4 < v < 1.6  | 
| P8 voltage: | 1.4 < v < 1.6  |   
| P9 voltage: | 1.4 < v < 1.6  | 
| P5 state:   | False          |  
| P6 state:   | False          | 
#### Step 3
1. Connect with a cable P2 pin to P7 pin.
2. Launch the second section

You should see the following result:
| Pin         | result         |
|-------------|----------------|
| P1 voltage: | 1.4 < v < 1.6  | 
| P7 voltage: | v > 3.0v       | 
| P8 voltage: | 1.4 < v < 1.6  |   
| P9 voltage: | 1.4 < v < 1.6  | 
| P5 state:   | False          |  
| P6 state:   | False          | 
#### Step 4
1. Connect with a cable P2 pin to P8 pin.
2. Launch the second section

You should see the following result:
| Pin         | result         |
|-------------|----------------|
| P1 voltage: | 1.4 < v < 1.6  | 
| P7 voltage: | 1.4 < v < 1.6  | 
| P8 voltage: | v > 3.0v  |   
| P9 voltage: | 1.4 < v < 1.6  | 
| P5 state:   | False          |  
| P6 state:   | False          | 
#### Step 5
1. Connect with a cable P2 pin to P9 pin.
2. Launch the second section

You should see the following result:
| Pin         | result         |
|-------------|----------------|
| P1 voltage: | 1.4 < v < 1.6  | 
| P7 voltage: | 1.4 < v < 1.6  | 
| P8 voltage: | 1.4 < v < 1.6  |   
| P9 voltage: | v > 3.0v       | 
| P5 state:   | False          |  
| P6 state:   | False          | 
#### Step 6
1. Connect with a cable P2 pin to P5 pin.
2. Launch the second section

You should see the following result:
| Pin         | result         |
|-------------|----------------|
| P1 voltage: | 1.4 < v < 1.6  | 
| P7 voltage: | 1.4 < v < 1.6  | 
| P8 voltage: | 1.4 < v < 1.6  |   
| P9 voltage: | 1.4 < v < 1.6  | 
| P5 state:   | True           |  
| P6 state:   | False          | 
#### Step 7
1. Connect with a cable P2 pin to P6 pin.
2. Launch the second section

You should see the following result:
| Pin         | result         |
|-------------|----------------|
| P1 voltage: | 1.4 < v < 1.6  | 
| P7 voltage: | 1.4 < v < 1.6  | 
| P8 voltage: | 1.4 < v < 1.6  |   
| P9 voltage: | 1.4 < v < 1.6  | 
| P5 state:   | False          |  
| P6 state:   | True           | 