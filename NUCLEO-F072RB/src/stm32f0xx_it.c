/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    stm32f0xx_it.c
  * @brief   Interrupt Service Routines.
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
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f0xx_it.h"
/* Private includes ----------------------------------------------------------*/

/******************************************************************************/
/*           Cortex-M0 Processor Interruption and Exception Handlers          */
/******************************************************************************/
/**
  * @brief This function handles Non maskable interrupt.
  */
void NMI_Handler(void)
{
}

/**
  * @brief This function handles Hard fault interrupt.
  */
void HardFault_Handler(void)
{
    while (1)
    {
    }
}

/**
  * @brief This function handles System service call via SWI instruction.
  */
void SVC_Handler(void)
{
}

/**
  * @brief This function handles Pendable request for system service.
  */
void PendSV_Handler(void)
{
}

/**
  * @brief This function handles System tick timer.
  */
void SysTick_Handler(void)
{
    HAL_IncTick();
}

/******************************************************************************/
/* STM32F0xx Peripheral Interrupt Handlers                                    */
/* Add here the Interrupt Handlers for the used peripherals.                  */
/* For the available peripheral interrupt handler names,                      */
/* please refer to the startup file (startup_stm32f0xx.s).                    */
/******************************************************************************/
void EXTI4_15_IRQHandler(void)
{
#ifdef PTP_DISABLED
    return;
#endif

    uint32_t pending = EXTI->PR;
    if (pending & PTPA_PIN)
    {
        HAL_GPIO_EXTI_IRQHandler(PTPA_PIN);
    }

#if defined(PTP_CONFIG_AB) || defined(PTP_CONFIG_AC) || defined(PTP_CONFIG_AD) || defined(PTP_CONFIG_BC) || defined(PTP_CONFIG_BD) || defined(PTP_CONFIG_CD)
    if (pending & PTPB_PIN)
    {
        HAL_GPIO_EXTI_IRQHandler(PTPB_PIN);
    }
#endif
}

void EXTI2_3_IRQHandler(void)
{
}
/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
