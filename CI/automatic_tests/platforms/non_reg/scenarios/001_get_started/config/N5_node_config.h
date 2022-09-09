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
 *     a default configuration, for specific MCU family, in luos_hal_config.h.
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
 * FLASH CONFIGURATION FOR APP WITH BOOTLOADER
 ********************************************************************************
 *    Define                | Default Value              | Description
 *    :---------------------|------------------------------------------------------
 *    BOOT_START_ADDRESS    | FLASH_BASE = 0x8000000     | Start address of Bootloader in flash
 *    SHARED_MEMORY_ADDRESS | 0x0800C000                 | Start address of shared memory to save boot flag
 *    APP_START_ADDRESS     | 0x0800C800                 | Start address of application with bootloader
 *    APP_END_ADDRESS       | FLASH_END                  | End address of application with bootloader
 ******************************************************************************/

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
 *    MAX_SERVICE_NUMBER    |              5             | Service number in the
 *node MSG_BUFFER_SIZE       | 3*SIZE_MSG_MAX (405 Bytes) | Size in byte of the
 *Luos buffer TX and RX MAX_MSG_NB            |   2*MAX_SERVICE_NUMBER   |
 *Message number in Luos buffer NBR_PORT              |              2 | PTP
 *Branch number Max 8 NBR_RETRY             |              10            | Send
 *Retry number in case of NACK or collision
 ******************************************************************************/
#define MAX_SERVICE_NUMBER 5
#define MAX_MSG_NB         40
#define MSG_BUFFER_SIZE    1024

/*******************************************************************************
 * LUOS HAL LIBRARY DEFINITION
*******************************************************************************
 *    Define                  | Description
 *    :-----------------------|-----------------------------------------------
 *    MCUFREQ                 | Put your the MCU frequency (value in Hz)
 *    TIMERDIV                | Timer divider clock (see your clock
configuration)
 *    USE_CRC_HW              | define to 0 if there is no Module CRC in your
MCU
 *    USE_TX_IT               | define to 1 to not use DMA transfers for Luos Tx
 *
 *    PORT_CLOCK_ENABLE       | Enable clock for port
 *    PTPx                    | A,B,C,D etc. PTP Branch Pin/Port/IRQ
 *    TX_LOCK_DETECT          | Disable by default use if not busy flag in USART
Pin/Port/IRQ
 *    RX_EN                   | Rx enable for driver RS485 always on Pin/Port
 *    TX_EN                   | Tx enable for driver RS485 Pin/Port
 *    COM_TX                  | Tx USART Com Pin/Port/Alternate
 *    COM_RX                  | Rx USART Com Pin/Port/Alternate
 *    PINOUT_IRQHANDLER       | Callback function for Pin IRQ handler

 *    LUOS_COM_CLOCK_ENABLE   | Enable clock for USART
 *    LUOS_COM                | USART number
 *    LUOS_COM_IRQ            | USART IRQ number
 *    LUOS_COM_IRQHANDLER     | Callback function for USART IRQ handler

 *    LUOS_DMA_CLOCK_ENABLE   | Enable clock for DMA
 *    LUOS_DMA                | DMA number
 *    LUOS_DMA_CHANNEL        | DMA channel (depending on MCU DMA may need
special config)

 *    LUOS_TIMER_CLOCK_ENABLE | Enable clock for Timer
 *    LUOS_TIMER              | Timer number
 *    LUOS_TIMER_IRQ          | Timer IRQ number
 *    LUOS_TIMER_IRQHANDLER   | Callback function for Timer IRQ handler

 *    FLASH_SECTOR               | FLASH page size
 *    PAGE_SIZE               | FLASH page size
 *    ADDRESS_LAST_PAGE_FLASH | Page to write alias
******************************************************************************/
#define TX_EN_PIN  GPIO_PIN_15
#define TX_EN_PORT GPIOA

// !!!!!!!  DO NOT EDIT THE LINES BELOW  !!!!!!!
// !!!!!!!  DO NOT EDIT THE LINES BELOW  !!!!!!!
// !!!!!!!  DO NOT EDIT THE LINES BELOW  !!!!!!!

/*******************************************************************************
 * LUOS HAL CI DEFINITION (CONTINUOUS INTEGRATION)
 *******************************************************************************
 *    Define                  | Description
 *    :-----------------------|-----------------------------------------------
 *    PTP_CONFIG              | PTP configuration (multiplex A/B/C/D)
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
#define PTP_POWER_PIN  GPIO_PIN_0
#define PTP_POWER_PORT GPIOA
#define PTP_A          GPIO_PIN_4
#define PTP_A_PORT     GPIOB
#define PTP_B          GPIO_PIN_5
#define PTP_B_PORT     GPIOB
#define PTP_C          GPIO_PIN_1
#define PTP_C_PORT     GPIOA
#define PTP_D          GPIO_PIN_2
#define PTP_D_PORT     GPIOA
#define PTP_A_IRQ      EXTI4_IRQn
#define PTP_B_IRQ      EXTI9_5_IRQn
#define PTP_C_IRQ      EXTI1_IRQn
#define PTP_D_IRQ      EXTI2_IRQn
#define PTP_NO_IRQ     EXTI15_10_IRQn

// PTP_CONFIG_UNKNOWN below is modified by Luos CI python tool :
#define PTP_CONFIG_B // DO NOT EDIT THIS LINE !!!!!!!!!!!!!!!!!!!!!!!

// Depending on previous config values, declaration of PTP lines and RS485 power
// state
// -------------------------------------------------------------------------------------
#ifdef PTP_CONFIG_UNKNOWN
// Node is not connected to the network
#define PTPA_PIN  PTP_A
#define PTPA_PORT PTP_A_PORT
#define PTPB_PIN  PTP_B
#define PTPB_PORT PTP_B_PORT
#define PTPA_IRQ  PTP_NO_IRQ
#define PTPB_IRQ  PTP_NO_IRQ
#define PTP_DISABLED

#else
// Node is connected, the breakout boards must be powered on
#define PTP_POWER
#endif

// PTP A
#ifdef PTP_CONFIG_A
#define PTPA_PIN  PTP_A
#define PTPA_PORT PTP_A_PORT
#define PTPA_IRQ  PTP_A_IRQ
#define PTPB_PIN  PTP_B
#define PTPB_PORT PTP_B_PORT
#define PTPB_IRQ  PTP_NO_IRQ
#endif

// PTP B
#ifdef PTP_CONFIG_B
#define PTPA_PIN  PTP_B
#define PTPA_PORT PTP_B_PORT
#define PTPA_IRQ  PTP_B_IRQ
#define PTPB_PIN  PTP_D
#define PTPB_PORT PTP_D_PORT
#define PTPB_IRQ  PTP_NO_IRQ
#endif

// PTP C
#ifdef PTP_CONFIG_C
#define PTPA_PIN  PTP_C
#define PTPA_PORT PTP_C_PORT
#define PTPA_IRQ  PTP_C_IRQ
#define PTPB_PIN  PTP_D
#define PTPB_PORT PTP_D_PORT
#define PTPB_IRQ  PTP_NO_IRQ
#endif

// PTP D
#ifdef PTP_CONFIG_D
#define PTPA_PIN  PTP_D
#define PTPA_PORT PTP_D_PORT
#define PTPA_IRQ  PTP_D_IRQ
#define PTPB_PIN  PTP_B
#define PTPB_PORT PTP_B_PORT
#define PTPB_IRQ  PTP_NO_IRQ
#endif

// PTP A and B
#ifdef PTP_CONFIG_AB
#define PTPA_PIN  PTP_A
#define PTPA_PORT PTP_A_PORT
#define PTPA_IRQ  PTP_A_IRQ
#define PTPB_PIN  PTP_B
#define PTPB_PORT PTP_B_PORT
#define PTPB_IRQ  PTP_B_IRQ
#endif

// PTP C and D
#ifdef PTP_CONFIG_CD
#define PTPA_PIN  PTP_C
#define PTPA_PORT PTP_C_PORT
#define PTPA_IRQ  PTP_C_IRQ
#define PTPB_PIN  PTP_D
#define PTPB_PORT PTP_D_PORT
#define PTPB_IRQ  PTP_D_IRQ
#endif

// PTP A and C
#ifdef PTP_CONFIG_AC
#define PTPA_PIN  PTP_A
#define PTPA_PORT PTP_A_PORT
#define PTPA_IRQ  PTP_A_IRQ
#define PTPB_PIN  PTP_C
#define PTPB_PORT PTP_C_PORT
#define PTPB_IRQ  PTP_C_IRQ
#endif

// PTP A and D
#ifdef PTP_CONFIG_AD
#define PTPA_PIN  PTP_A
#define PTPA_PORT PTP_A_PORT
#define PTPA_IRQ  PTP_A_IRQ
#define PTPB_PIN  PTP_D
#define PTPB_PORT PTP_D_PORT
#define PTPB_IRQ  PTP_D_IRQ
#endif

// PTP B and C
#ifdef PTP_CONFIG_BC
#define PTPA_PIN  PTP_B
#define PTPA_PORT PTP_B_PORT
#define PTPA_IRQ  PTP_B_IRQ
#define PTPB_PIN  PTP_C
#define PTPB_PORT PTP_C_PORT
#define PTPB_IRQ  PTP_C_IRQ
#endif

// PTP B and D
#ifdef PTP_CONFIG_BD
#define PTPA_PIN  PTP_B
#define PTPA_PORT PTP_B_PORT
#define PTPA_IRQ  PTP_B_IRQ
#define PTPB_PIN  PTP_D
#define PTPB_PORT PTP_D_PORT
#define PTPB_IRQ  PTP_D_IRQ
#endif
#endif /* _NODE_CONFIG_H_ */
