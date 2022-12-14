set(BOARD_ROOT "${CMAKE_CURRENT_SOURCE_DIR}")

cmake_minimum_required(VERSION 3.13.1)

include($ENV{ZEPHYR_BASE}/cmake/app/boilerplate.cmake NO_POLICY_SCOPE)

project(get_started)

# Get Started
target_sources(app PRIVATE ../src/main.c)

# target_sources(app PRIVATE ../src/stm32l4xx_hal_msp.c)
# target_sources(app PRIVATE ../src/stm32l4xx_it.c)
# target_sources(app PRIVATE ../lib/Button/button.c)
