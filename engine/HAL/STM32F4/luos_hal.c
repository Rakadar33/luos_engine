/******************************************************************************
 * @file luosHAL
 * @brief Luos Hardware Abstration Layer. Describe Low layer fonction
 * @MCU Family STM32F4
 * @author Luos
 * @version 0.0.0
 ******************************************************************************/
#include "luos_hal.h"

#include <stdbool.h>
#include <string.h>
#include "reception.h"
#include "context.h"

// MCU dependencies this HAL is for family STM32F4 you can find
// the HAL stm32cubeF4 on ST web site
#include "stm32f4xx_ll_system.h"

/*******************************************************************************
 * Variables
 ******************************************************************************/
// timestamp variable
static ll_timestamp_t ll_timestamp;
/*******************************************************************************
 * Function
 ******************************************************************************/
static void LuosHAL_SystickInit(void);
static void LuosHAL_FlashInit(void);
static void LuosHAL_VectorTableRemap(void);

/////////////////////////Luos Library Needed function///////////////////////////

/******************************************************************************
 * @brief Luos HAL general initialisation
 * @param None
 * @return None
 ******************************************************************************/
void LuosHAL_Init(void)
{
    // Remap Vector Table
    LuosHAL_VectorTableRemap();

    // Systick Initialization
    LuosHAL_SystickInit();

    // Flash Initialization
    LuosHAL_FlashInit();

    // start timestamp
    LuosHAL_StartTimestamp();
}
/******************************************************************************
 * @brief Luos HAL general disable IRQ
 * @param None
 * @return None
 ******************************************************************************/
_CRITICAL void LuosHAL_SetIrqState(uint8_t Enable)
{
    if (Enable == true)
    {
        __enable_irq();
    }
    else
    {
        __disable_irq();
    }
}
/******************************************************************************
 * @brief Luos HAL general systick tick at 1ms initialize
 * @param None
 * @return tick Counter
 ******************************************************************************/
static void LuosHAL_SystickInit(void)
{
}

/******************************************************************************
 * @brief Luos HAL remap Vector table in given address in flash
 * @param None
 * @return None
 ******************************************************************************/
static void LuosHAL_VectorTableRemap(void)
{
    SCB->VTOR = LUOS_VECT_TAB;
}
/******************************************************************************
 * @brief Luos HAL general systick tick at 1ms
 * @param None
 * @return tick Counter
 ******************************************************************************/
_CRITICAL uint32_t LuosHAL_GetSystick(void)
{
    return HAL_GetTick();
}

/******************************************************************************
 * @brief Luos GetTimestamp
 * @param None
 * @return uint64_t
 ******************************************************************************/
_CRITICAL uint64_t LuosHAL_GetTimestamp(void)
{
    ll_timestamp.lower_timestamp  = (SysTick->LOAD - SysTick->VAL) * (1000000000 / MCUFREQ);
    ll_timestamp.higher_timestamp = (uint64_t)(LuosHAL_GetSystick() - ll_timestamp.start_offset);

    return ll_timestamp.higher_timestamp * 1000000 + (uint64_t)ll_timestamp.lower_timestamp;
}

/******************************************************************************
 * @brief Luos start Timestamp
 * @param None
 * @return None
 ******************************************************************************/
_CRITICAL void LuosHAL_StartTimestamp(void)
{
    ll_timestamp.start_offset = LuosHAL_GetSystick();
}

/******************************************************************************
 * @brief Luos stop Timestamp
 * @param None
 * @return None
 ******************************************************************************/
_CRITICAL void LuosHAL_StopTimestamp(void)
{
    ll_timestamp.lower_timestamp  = 0;
    ll_timestamp.higher_timestamp = 0;
    ll_timestamp.start_offset     = 0;
}

/******************************************************************************
 * @brief Flash Initialisation
 * @param None
 * @return None
 ******************************************************************************/
static void LuosHAL_FlashInit(void)
{
}
/******************************************************************************
 * @brief Set boot mode in shared flash memory
 * @param
 * @return
 ******************************************************************************/
_CRITICAL void LuosHAL_SetMode(uint8_t mode)
{
    uint32_t data_to_write = ~BOOT_MODE_MASK | (mode << BOOT_MODE_OFFSET);

    uint32_t sector_error = 0;
    FLASH_EraseInitTypeDef s_eraseinit;

    s_eraseinit.TypeErase    = FLASH_TYPEERASE_SECTORS;
    s_eraseinit.VoltageRange = FLASH_VOLTAGE_RANGE_3;
    s_eraseinit.NbSectors    = 1;
    s_eraseinit.Sector       = SHARED_MEMORY_SECTOR;

    /****************************** WARNING ***************************************
     * when STRT bit in FLASH->CR register is called from the app (sector 4 in flash)
     * the application crashes, that's why we only erase the flash from the
     * bootloader
     ******************************* WARNING **************************************/
    if (mode != 0x02)
    {
        // erase sector
        HAL_FLASH_Unlock();
        HAL_FLASHEx_Erase(&s_eraseinit, &sector_error);
        HAL_FLASH_Lock();
    }

    // write sector
    HAL_FLASH_Unlock();
    HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, (uint32_t)SHARED_MEMORY_ADDRESS, data_to_write);
    HAL_FLASH_Lock();
}

/******************************************************************************
 * @brief Save node ID in shared flash memory
 * @param Address, node_id
 * @return
 ******************************************************************************/
_CRITICAL void LuosHAL_SaveNodeID(uint16_t node_id)
{
    uint32_t *p_start      = (uint32_t *)SHARED_MEMORY_ADDRESS;
    uint32_t saved_data    = *p_start;
    uint32_t data_tmp      = ~NODE_ID_MASK | (node_id << NODE_ID_OFFSET);
    uint32_t data_to_write = saved_data & data_tmp;

    // write sector
    HAL_FLASH_Unlock();
    HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, (uint32_t)SHARED_MEMORY_ADDRESS, data_to_write);
    HAL_FLASH_Lock();
}

/******************************************************************************
 * @brief software reboot the microprocessor
 * @param
 * @return
 ******************************************************************************/
void LuosHAL_Reboot(void)
{
    // DeInit RCC and HAL
    HAL_RCC_DeInit();
    HAL_DeInit();

    // reset systick
    SysTick->CTRL = 0;
    SysTick->LOAD = 0;
    SysTick->VAL  = 0;

    // reset in bootloader mode
    NVIC_SystemReset();
}

/******************************************************************************
 * @brief DeInit Bootloader peripherals
 * @param
 * @return
 ******************************************************************************/
typedef void (*pFunction)(void); /*!< Function pointer definition */

void LuosHAL_JumpToAddress(uint32_t addr)
{
    uint32_t JumpAddress = *(__IO uint32_t *)(addr + 4);
    pFunction Jump       = (pFunction)JumpAddress;

    __disable_irq();

    SysTick->CTRL = 0;
    SysTick->LOAD = 0;
    SysTick->VAL  = 0;

    SCB->VTOR = addr;

    __set_MSP(*(__IO uint32_t *)addr);

    __enable_irq();

    Jump();
}

/******************************************************************************
 * @brief Return bootloader mode saved in flash
 * @param
 * @return
 ******************************************************************************/
uint8_t LuosHAL_GetMode(void)
{
    uint32_t *p_start = (uint32_t *)SHARED_MEMORY_ADDRESS;
    uint32_t data     = (*p_start & BOOT_MODE_MASK) >> BOOT_MODE_OFFSET;

    return (uint8_t)data;
}

#ifdef BOOTLOADER
/******************************************************************************
 * @brief DeInit Bootloader peripherals
 * @param
 * @return
 ******************************************************************************/
void LuosHAL_DeInit(void)
{
    HAL_RCC_DeInit();
    HAL_DeInit();
}

/******************************************************************************
 * @brief Get node id saved in flash memory
 * @param Address
 * @return node_id
 ******************************************************************************/
uint16_t LuosHAL_GetNodeID(void)
{
    uint32_t *p_start = (uint32_t *)SHARED_MEMORY_ADDRESS;
    uint32_t data     = *p_start & NODE_ID_MASK;
    uint16_t node_id  = (uint16_t)(data >> NODE_ID_OFFSET);

    return node_id;
}

/******************************************************************************
 * @brief erase sectors in flash memory
 * @param Address, size
 * @return
 ******************************************************************************/
void LuosHAL_EraseMemory(uint32_t address, uint16_t size)
{
    uint32_t nb_sectors_to_erase = APP_END_SECTOR - APP_START_SECTOR + 1;
    uint32_t sector_to_erase     = APP_START_SECTOR;

    uint32_t sector_error = 0;
    FLASH_EraseInitTypeDef s_eraseinit;
    s_eraseinit.TypeErase    = FLASH_TYPEERASE_SECTORS;
    s_eraseinit.VoltageRange = FLASH_VOLTAGE_RANGE_3;
    s_eraseinit.NbSectors    = 1;

    int i = 0;
    for (i = 0; i < nb_sectors_to_erase; i++)
    {
        s_eraseinit.Sector = sector_to_erase;

        // Unlock flash
        HAL_FLASH_Unlock();
        // Erase Page
        HAL_FLASHEx_Erase(&s_eraseinit, &sector_error);
        // re-lock FLASH
        HAL_FLASH_Lock();

        // update page to erase
        sector_to_erase += 1;
    }
}

/******************************************************************************
 * @brief Save binary data in shared flash memory
 * @param Address, size, data[]
 * @return
 ******************************************************************************/
void LuosHAL_ProgramFlash(uint32_t address, uint16_t size, uint8_t *data)
{
    // Unlock flash
    HAL_FLASH_Unlock();
    // ST hal flash program function write data by uint64_t raw data
    for (uint32_t i = 0; i < size; i += sizeof(uint32_t))
    {
        while (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, i + address, *(uint32_t *)(&data[i])) != HAL_OK)
            ;
    }
    // re-lock FLASH
    HAL_FLASH_Lock();
}
#endif
