/******************************************************************************
 * @file luosHAL_Config
 * @brief This file allow you to configure LuosHAL according to your design
 *        this is the default configuration created by Luos team for this MCU
 *Family Do not modify this file if you want to ovewrite change define in you
 *project
 * @MCU Family STM32FO
 * @author Luos
 * @version 0.0.0
 ******************************************************************************/
#ifndef _BOARD_CONFIG_H_

// No Hardware CRC
#define USE_CRC_HW 0

// PTP pin definition
#define PTPA_PIN GPIO_PIN_5
#define PTPA_PORT GPIOB

#define PTPB_PIN GPIO_PIN_4
#define PTPB_PORT GPIOB

#define PTPA_IRQ EXTI4_15_IRQn
#define PTPB_IRQ EXTI4_15_IRQn

// COM pin definition
#define RX_EN_PIN GPIO_PIN_7
#define RX_EN_PORT GPIOB

#define TX_EN_PIN GPIO_PIN_1
#define TX_EN_PORT GPIOB

// TIMER pin definition
#define LUOS_TIMER_CLOCK_ENABLE() __HAL_RCC_TIM3_CLK_ENABLE()
#define LUOS_TIMER TIM3
#define LUOS_TIMER_IRQ TIM3_IRQn
#define LUOS_TIMER_IRQHANDLER() TIM3_IRQHandler()

// redefinitions
#undef MS1_Pin
#define MS1_Pin GPIO_PIN_7
#undef MS1_GPIO_Port
#define MS1_GPIO_Port GPIOA
#undef MS2_Pin
#define MS2_Pin GPIO_PIN_7
#undef MS2_GPIO_Port
#define MS2_GPIO_Port GPIOA
#undef MS3_Pin
#define MS3_Pin GPIO_PIN_7
#undef MS3_GPIO_Port
#define MS3_GPIO_Port GPIOA
#undef EN_Pin
#define EN_Pin GPIO_PIN_7
#undef EN_GPIO_Port
#define EN_GPIO_Port GPIOA
#undef LED_GPIO_Port
#define LED_GPIO_Port GPIOB
#undef LED_PIN
#define LED_PIN GPIO_PIN_3
#define POS_Pin GPIO_PIN_1
#define POS_GPIO_Port GPIOA
#define LIGHT_Pin GPIO_PIN_7
#define LIGHT_GPIO_Port GPIOA

#endif /* _BOARD_CONFIG_H_ */
