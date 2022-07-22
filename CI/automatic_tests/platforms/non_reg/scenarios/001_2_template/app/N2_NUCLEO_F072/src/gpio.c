/**
 ******************************************************************************
 * File Name          : gpio.c
 * Description        : This file provides code for the configuration
 *                      of all used GPIO pins.
 ******************************************************************************
 * @attention
 *
 * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
 * All rights reserved.</center></h2>
 *
 * This software component is licensed by ST under BSD 3-Clause license,
 * the "License"; You may not use this file except in compliance with the
 * License. You may obtain a copy of the License at:
 *                        opensource.org/licenses/BSD-3-Clause
 *
 ******************************************************************************
 */

/* Includes ------------------------------------------------------------------*/
#include "gpio.h"
#include "luos_hal.h"

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/*----------------------------------------------------------------------------*/
/* Configure GPIO                                                             */
/*----------------------------------------------------------------------------*/
/* USER CODE BEGIN 1 */

/* USER CODE END 1 */

/** Configure pins
     PA0   ------> ADC_IN0
     PA2   ------> ADC_IN2
*/
void MX_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    /* GPIO Ports Clock Enable */
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();

    GPIO_InitStruct.Pin   = LED_Pin;
    GPIO_InitStruct.Mode  = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull  = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(LED_GPIO_Port, &GPIO_InitStruct);
}

/* USER CODE BEGIN 2 */
void PTP_Power_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    // By default, PTP Power is OFF
    HAL_GPIO_WritePin(PTP_POWER_PORT, PTP_POWER_PIN, GPIO_PIN_RESET);
    GPIO_InitStruct.Pin   = PTP_POWER_PIN;
    GPIO_InitStruct.Mode  = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull  = GPIO_PULLDOWN;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(PTP_POWER_PORT, &GPIO_InitStruct);
}

void PTP_Power_Config(void)
{
#ifdef PTP_POWER
    HAL_GPIO_WritePin(PTP_POWER_PORT, PTP_POWER_PIN, GPIO_PIN_SET);
#endif
}

void Led_blink(uint32_t *tickstart)
{
    static GPIO_PinState LedPinState = GPIO_PIN_RESET;
    // LED blinks each second
    if ((LuosHAL_GetSystick() - *tickstart) > 1000)
    {
        *tickstart  = LuosHAL_GetSystick();
        LedPinState = ~(LedPinState);
        HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, LedPinState);
    }
}
/* USER CODE END 2 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
