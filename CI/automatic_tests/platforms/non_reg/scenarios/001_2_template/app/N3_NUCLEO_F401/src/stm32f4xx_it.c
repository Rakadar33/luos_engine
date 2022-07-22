/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    stm32f4xx_it.c
  * @brief   Interrupt Service Routines.
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
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f4xx_it.h"

/******************************************************************************/
/*           Cortex-M4 Processor Interruption and Exception Handlers          */
/******************************************************************************/
/**
  * @brief This function handles Non maskable interrupt.
  */
void NMI_Handler(void)
{
    while (1)
    {
    }
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
  * @brief This function handles Memory management fault.
  */
void MemManage_Handler(void)
{
    while (1)
    {
    }
}

/**
  * @brief This function handles Pre-fetch fault, memory access fault.
  */
void BusFault_Handler(void)
{
    while (1)
    {
    }
}

/**
  * @brief This function handles Undefined instruction or illegal state.
  */
void UsageFault_Handler(void)
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
  * @brief This function handles Debug monitor.
  */
void DebugMon_Handler(void)
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
/* STM32F4xx Peripheral Interrupt Handlers                                    */
/* Add here the Interrupt Handlers for the used peripherals.                  */
/* For the available peripheral interrupt handler names,                      */
/* please refer to the startup file (startup_stm32f4xx.s).                    */
/******************************************************************************/
void EXTI4_IRQHandler(void)
{
    //DEBUG
    static uint8_t dbg = 0;
    dbg++;

    #ifdef PTP_DISABLED
    return;
    #endif

    #if defined(PTP_CONFIG_A) || defined(PTP_CONFIG_AB) || defined(PTP_CONFIG_AC) || defined(PTP_CONFIG_AD)
    HAL_GPIO_EXTI_IRQHandler(PTPA_PIN);
    #endif
}

void EXTI9_5_IRQHandler(void)
{
    //DEBUG
    static uint8_t dbg = 0;
    dbg++;

    #ifdef PTP_DISABLED
    return;
    #endif

    #if defined(PTP_CONFIG_B) || defined(PTP_CONFIG_BC) || defined(PTP_CONFIG_BD)
    HAL_GPIO_EXTI_IRQHandler(PTPA_PIN);
    #endif

    #if defined(PTP_CONFIG_AB)
    HAL_GPIO_EXTI_IRQHandler(PTPB_PIN);
    #endif
}

void EXTI15_10_IRQHandler(void)
{
    //DEBUG
    static uint8_t dbg = 0;
    dbg++;

    #ifdef PTP_DISABLED
    return;
    #endif

    #if defined(PTP_CONFIG_C) || defined(PTP_CONFIG_D)
    HAL_GPIO_EXTI_IRQHandler(PTPA_PIN);
    #endif

    #if defined(PTP_CONFIG_AC) || defined(PTP_CONFIG_AD) || defined(PTP_CONFIG_BC) || defined(PTP_CONFIG_BD)
    HAL_GPIO_EXTI_IRQHandler(PTPB_PIN);
    #endif

    #if defined(PTP_CONFIG_CD)
    uint32_t pending = EXTI->PR1;
    if(pending & (1 << PTPA_PIN))
    {
        HAL_GPIO_EXTI_IRQHandler(PTPA_PIN);        
    }
    if(pending & (1 << PTPB_PIN))
    {
        HAL_GPIO_EXTI_IRQHandler(PTPB_PIN);        
    }
    #endif

}

void EXTI3_IRQHandler(void)
{
    //DEBUG
    static uint8_t dbg = 0;
    dbg++;
}

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
