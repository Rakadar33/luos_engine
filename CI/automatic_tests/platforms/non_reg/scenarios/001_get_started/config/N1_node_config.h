/******************************************************************************
 * @file node_config.h
 * @brief This file allow you to use standard preprocessor definitions to
 *        configure your project, Luos and Luos HAL libraries
 *
 *   # Introduction
 *     This file is for the luos user. You may here configure your project and
 *     define your custom Luos service and custom Luos command for your product
 *
 *     Luos libraries offer a minimal standard configuration to optimize
 *     memory usage. In some case you have to modify standard value to fit
 *     with your need concerning among of data transiting through the network
 *     or network speed for example
 *
 *     Luos libraries can be use with a lot a MCU family. Luos compagny give you
 *     a default configuration, for specific MCU family, in robus_hal_config.h.
 *     This configuration can be modify here to fit with you design by
 *     preprocessor definitions of MCU Hardware needs
 *
 *   # Usage
 *      This file should be place a the root folder of your project and include
 *      where build flag preprocessor definitions are define in your IDE
 *      -include node_config.h
 *
 * @author Luos
 * @version 0.0.0
 ******************************************************************************/
#ifndef _NODE_CONFIG_H_
#define _NODE_CONFIG_H_

/*******************************************************************************
 * PROJECT DEFINITION
 *******************************************************************************/

/*******************************************************************************
 * OTHER GATE PARAMETERS
 *******************************************************************************
 *    Define                    | Default Value              | Description
 *    :-------------------------|------------------------------------------------------
 *    INIT_TIME                 |              150           | Wait init time before first detection
 * ******************************************************************************/
#define INIT_TIME 150

/*******************************************************************************
 * LUOS LIBRARY DEFINITION
 *******************************************************************************
 *    Define                | Default Value              | Description
 *    :---------------------|------------------------------------------------------
 *    MAX_SERVICE_NUMBER    |              5             | Service number in the node
 *    MSG_BUFFER_SIZE       | 3*SIZE_MSG_MAX (405 Bytes) | Size in byte of the Luos buffer TX and RX
 *    MAX_MSG_NB            |   2*MAX_SERVICE_NUMBER   | Message number in Luos buffer
 *    NBR_PORT              |              2             | PTP Branch number Max 8
 *    NBR_RETRY             |              10            | Send Retry number in case of NACK or collision
 ******************************************************************************/
#define MAX_SERVICE_NUMBER 5
#define MAX_MSG_NB         40
//#define NODETECTION

/*******************************************************************************
 * GATE SERIAL COM DEFINITION
 *******************************************************************************
 *    Define                    | Default Value              | Description
 *    :-------------------------|------------------------------------------------------
 *    MAX_RTB_ENTRY             |              40            | max number entry
 *in routing table GATE_BUFF_SIZE            |             1024           | Json
 *receive buffer size PIPE_TO_LUOS_BUFFER_SIZE  |             1024           |
 *Receive pipe buffer size LUOS_TO_PIPE_BUFFER_SIZE  |             2048 |
 *Transmit pipe buffer size
 ******************************************************************************/
#define MAX_RTB_ENTRY            40
#define GATE_BUFF_SIZE           1024
#define PIPE_TO_LUOS_BUFFER_SIZE 1024
#define LUOS_TO_PIPE_BUFFER_SIZE 2048

// !!!!!!!  DO NOT EDIT THE LINES BELOW  !!!!!!!
// !!!!!!!  DO NOT EDIT THE LINES BELOW  !!!!!!!
// !!!!!!!  DO NOT EDIT THE LINES BELOW  !!!!!!!

/*******************************************************************************
 * LUOS HAL CI DEFINITION (CONTINUOUS INTEGRATION)
 *******************************************************************************
 *    Define                  | Description
 *    :-----------------------|-----------------------------------------------
 *    PTP_CONFIG              |z PTP configuration (multiplex A/B/C/D)
 *******************************************************************************
 *
 * PTP_CONFIG_UNKNOWN is modified by Luos CI python tool
 *
 * PTP_CONFIG possible values:
 *
 * 1) If not defined:
 *     - The 2 breakout boards are powered OFF
 *     - All PTP lines are OFF
 *
 *  2) If PTP_CONFIG_XY:
 *     - The 2 breakout boards are powered ON
 *     - PTP lines X and Y are ON
 *     - Others PTP lines are OFF
 *****************************************************************************/
// PTP definitions
#define PTP_POWER_PIN 5
#define PTP_A         6
#define PTP_B         7
#define PTP_C         1
#define PTP_D         4

// PTP_CONFIG_UNKNOWN below is modified by Luos CI python tool :
#define PTP_CONFIG_A // DO NOT EDIT THIS LINE !!!!!!!!!!!!!!!!!!!!!!!

// Depending on previous config values, declaration of PTP lines and RS485 power
// state
// -------------------------------------------------------------------------------------
#ifdef PTP_CONFIG_UNKNOWN
// Node is not connected to the network
#define ARDUINO_PTPA_PIN 2 //TODO : VERIFY
#define ARDUINO_PTPB_PIN 2 //TODO : VERIFY
#define PTP_DISABLED

#else
// Node is connected, the breakout boards must be powered on
#define PTP_POWER
#endif

// PTP A
#ifdef PTP_CONFIG_A
#define ARDUINO_PTPA_PIN PTP_A
#define ARDUINO_PTPB_PIN PTP_B
#endif

// PTP B
#ifdef PTP_CONFIG_B
#define ARDUINO_PTPA_PIN PTP_B
#define ARDUINO_PTPB_PIN PTP_D
#endif

// PTP C
#ifdef PTP_CONFIG_C
#define ARDUINO_PTPA_PIN PTP_C
#define ARDUINO_PTPB_PIN PTP_D
#endif

// PTP D
#ifdef PTP_CONFIG_D
#define ARDUINO_PTPA_PIN PTP_D
#define ARDUINO_PTPB_PIN PTP_B
#endif

// PTP A and B
#ifdef PTP_CONFIG_AB
#define ARDUINO_PTPA_PIN PTP_A
#define ARDUINO_PTPB_PIN PTP_B
#endif

// PTP C and D
#ifdef PTP_CONFIG_CD
#define ARDUINO_PTPA_PIN PTP_C
#define ARDUINO_PTPB_PIN PTP_D
#endif

// PTP A and C
#ifdef PTP_CONFIG_AC
#define ARDUINO_PTPA_PIN PTP_A
#define ARDUINO_PTPB_PIN PTP_C
#endif

// PTP A and D
#ifdef PTP_CONFIG_AD
#define ARDUINO_PTPA_PIN PTP_A
#define ARDUINO_PTPB_PIN PTP_D
#endif

// PTP B and C
#ifdef PTP_CONFIG_BC
#define ARDUINO_PTPA_PIN PTP_B
#define ARDUINO_PTPB_PIN PTP_C
#endif

// PTP B and D
#ifdef PTP_CONFIG_BD
#define ARDUINO_PTPA_PIN PTP_B
#define ARDUINO_PTPB_PIN PTP_D
#endif

#endif /* _NODE_CONFIG_H_ */
