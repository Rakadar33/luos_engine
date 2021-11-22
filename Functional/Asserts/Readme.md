# Assert Test Description : 

## Functionality tested

Inspector Assert mechanism 

## Goal

This test aims to validate the assert mechanism developped for the functionalities of inspector. This assert mechanism stores each assert message received in the network, in a 2-dimensional buffer that can fit 3 complete Luos messages. In case of more than three assert messages the inspector keeps always the 3 last messages received, by removing the oldest one each time a new one arrives.

The test application sends to the network a predefined maximum number of false assert messages each second after the detection of the network, and the goal is that the inspector stores them and sends to the computer the last three messages at the moment that the high level demands it with a specific command.

## Details

The assert test application named assert_app works as any other Luos application, it has 2 functions that should be called in the Project "Assert_Init()" and "Assert_Loop()", and its only function is to send messages of command "ASSERT" = 0X04. The size of the data of these messages is 1, and the data is always the number of each assert message (0 - MAX_ASSERT_MSG) for debugging reasons.

## Setup

This test uses a Gate or any other service that launches a detection, the Inspector that monitors the messages in the network, and a third project (empty application or any other project like Button etc.) that includes the Assert_app. The "assert_app.h" should be included and th "Assert_Init()" and "Assert_Loop()" function should be called in the main.c of the project. Also make sure that you include the path of the assert_app folder in the platformio.ini of the project and that you increase the MAX_SERVICE_NUMBER in case that the project includes also other services.

## Procedure

Once the hardware is flashed and ready and the network connected by 2 usb ports, open the .ipynb included in this folder.

#### Step 1 
Launch the first section, that launches a detection using the gate and you should see your network appear.
!! Attention !! You should be in the branch of pyluos sniffer_2.0.0/inspector as it's not merge in master branch for now. 
Be sure that you have well defined the usb ports for each one of the cards.
#### Step 2
Launch the second section, you should see that that the inspector is connected, and you should see a message with the routing table on saleae logic.
#### Step 3
Launch the third section and you should see all the assert messages sent through the pin connected to the usb board using saleae logic.

# The testing procedure will change when we will have the SAAS completed.
