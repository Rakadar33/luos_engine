# REM ULIPE :
# ---->  Zephyr serial driver
# ---->  Zephyr timer

# -----------------------------------------------------------------
# LUOS ENGINE BUTTON INTEGRATION WITH ZEPHYR
# -----------------------------------------------------------------

# A RAJOUTER???? Les liens vers directoris
# set(ZEPHYR_EXTRA_MODULES "path/to-zephyr-custom-module"  [...])

# Path to out-of-tree boards definitions
set(BOARD_ROOT "${CMAKE_CURRENT_SOURCE_DIR}")

cmake_minimum_required(VERSION 3.13.1)

include($ENV{ZEPHYR_BASE}/cmake/app/boilerplate.cmake NO_POLICY_SCOPE)

project(button)

target_sources(app PRIVATE ../src/main.c)

# REMETTRE !!!
# target_sources(app PRIVATE ../src/gpio_l4xx.c)
target_sources(app PRIVATE ../src/stm32l4xx_hal_msp.c)
target_sources(app PRIVATE ../src/stm32l4xx_it.c)
target_sources(app PRIVATE ../lib/Button/button.c)

# target_sources(app PRIVATE ../../../../../network/robus/HAL/STM32L4/robus_hal.c)
# target_sources(app PRIVATE ../../../../../network/robus/HAL/STM32L4/robus_hal.h)
# target_sources(app PRIVATE ../../../../../network/robus/HAL/STM32L4/robus_hal_config.h)

# target_sources(app PRIVATE ../../../../../engine/HAL/STM32L4/luos_hal.c)
# target_sources(app PRIVATE ../../../../../engine/HAL/STM32L4/luos_hal.h)
# target_sources(app PRIVATE ../../../../../engine/HAL/STM32L4/luos_hal_config.h)
target_sources(app PRIVATE ../../../../../engine/core/src/luos_engine.c)
target_sources(app PRIVATE ../../../../../engine/core/src/luos_utils.c)
target_sources(app PRIVATE ../../../../../engine/core/src/profile_core.c)
target_sources(app PRIVATE ../../../../../engine/core/src/routing_table.c)
target_sources(app PRIVATE ../../../../../engine/core/src/streaming.c)
target_sources(app PRIVATE ../../../../../engine/core/src/timestamp.c)
target_sources(app PRIVATE ../../../../../engine/core/inc/luos.h)
target_sources(app PRIVATE ../../../../../engine/core/inc/luos_engine.h)
target_sources(app PRIVATE ../../../../../engine/core/inc/luos_list.h)
target_sources(app PRIVATE ../../../../../engine/core/inc/luos_utils.h)
target_sources(app PRIVATE ../../../../../engine/core/inc/profile_core.h)
target_sources(app PRIVATE ../../../../../engine/core/inc/routing_table.h)
target_sources(app PRIVATE ../../../../../engine/core/inc/service_structs.h)
target_sources(app PRIVATE ../../../../../engine/core/inc/streaming.h)
target_sources(app PRIVATE ../../../../../engine/OD/luos_od.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_angular.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_control.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_electric.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_force.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_illuminance.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_linear.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_pid.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_pressure.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_ratio.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_temperature.h)
target_sources(app PRIVATE ../../../../../engine/OD/od_time.h)
target_sources(app PRIVATE ../../../../../network/robus/src/msg_alloc.c)
target_sources(app PRIVATE ../../../../../network/robus/src/port_manager.c)
target_sources(app PRIVATE ../../../../../network/robus/src/reception.c)
target_sources(app PRIVATE ../../../../../network/robus/src/robus.c)
target_sources(app PRIVATE ../../../../../network/robus/src/topic.c)
target_sources(app PRIVATE ../../../../../network/robus/src/transmission.c)
target_sources(app PRIVATE ../../../../../network/robus/inc/config.h)
target_sources(app PRIVATE ../../../../../network/robus/inc/context.h)
target_sources(app PRIVATE ../../../../../network/robus/inc/msg_alloc.h)
target_sources(app PRIVATE ../../../../../network/robus/inc/port_manager.h)
target_sources(app PRIVATE ../../../../../network/robus/inc/reception.h)
target_sources(app PRIVATE ../../../../../network/robus/inc/robus.h)
target_sources(app PRIVATE ../../../../../network/robus/inc/robus_struct.h)
target_sources(app PRIVATE ../../../../../network/robus/inc/topic.h)
target_sources(app PRIVATE ../../../../../network/robus/inc/transmission.h)

# HAL
target_sources(app PRIVATE ../../../../../engine/HAL/STM32L4/luos_hal.c)
target_sources(app PRIVATE ../../../../../engine/HAL/STM32L4/luos_hal.h)
target_sources(app PRIVATE ../../../../../engine/HAL/STM32L4/luos_hal_config.h)
target_sources(app PRIVATE ../../../../../network/robus/HAL/STM32L4/robus_hal.c)
target_sources(app PRIVATE ../../../../../network/robus/HAL/STM32L4/robus_hal.h)
target_sources(app PRIVATE ../../../../../network/robus/HAL/STM32L4/robus_hal_config.h)

# STOP REMETTRE !!! DEBUG JGA

# zephyr_library_sources_ifdef(CONFIG_USE_STM32_HAL_CORTEX drivers/src/stm32l4xx_hal_cortex.c)

# zephyr_library_sources_ifdef(CONFIG_USE_STM32_HAL_FLASH drivers/src/stm32l4xx_hal_flash.c)
# zephyr_library_sources_ifdef(CONFIG_USE_STM32_HAL_FLASH_EX drivers/src/stm32l4xx_hal_flash_ex.c)

# C:\Users\jerom\.platformio\packages\framework-zephyr\_pio\modules\hal\stm32\stm32cube\stm32l4xx\drivers\src

# SOC_SERIES_STM32L4X
# SOC_STM32L432XX
# ARM_MPU
# HW_STACK_PROTECTION
# SERIAL
# PINMUX
# GPIO
# CLOCK_CONTROL
# CONSOLE
# UART_CONSOLE
