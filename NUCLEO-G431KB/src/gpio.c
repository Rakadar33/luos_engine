/**
  ******************************************************************************
  * @file    gpio.c
  * @brief   This file provides code for the configuration
  *          of all used GPIO pins.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
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

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/*----------------------------------------------------------------------------*/
/* Configure GPIO                                                             */
/*----------------------------------------------------------------------------*/
/* USER CODE BEGIN 1 */

/* USER CODE END 1 */

/** Configure pins
*/
void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : PtPin */
  GPIO_InitStruct.Pin = BTN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(BTN_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : PtPin */
  GPIO_InitStruct.Pin = LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LED_GPIO_Port, &GPIO_InitStruct);
}


void Unused_PTP_config(void)
{
/* USER CODE BEGIN 2 */

// REMETTRE !!!

//#if !defined(PTP_CONFIG_D) && !defined(PTP_CONFIG_AD) && !defined(PTP_CONFIG_BD) && !defined(PTP_CONFIG_CD)
  /*If PTP D is unused, disable the line*/
  GPIO_InitTypeDef GPIO_InitStruct = {0};  
  GPIO_InitStruct.Pin = PTP_D;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  //GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(PTP_D_PORT, &GPIO_InitStruct);

  /*Configure GPIO pin Output Level */
  uint16_t a;
  for(a=0;a<10;a++)
  {
    HAL_GPIO_WritePin(PTP_D_PORT, PTP_D, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(PTP_D_PORT, PTP_D, GPIO_PIN_SET);
    HAL_GPIO_WritePin(PTP_D_PORT, PTP_D, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(PTP_D_PORT, PTP_D, GPIO_PIN_SET);    
  }
//#endif
}

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
/* USER CODE END 2 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
