# -----------------------------------------------------------------
# Project
# -----------------------------------------------------------------

# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.13.1)
include($ENV{ZEPHYR_BASE}/cmake/app/boilerplate.cmake NO_POLICY_SCOPE)

project(button)
target_sources(app PRIVATE ../src/main.c)

# ##   # Additional modules ??????????????????????????????????????????????????????????????????????????????
# ##   set(ZEPHYR_EXTRA_MODULES "path/to-zephyr-custom-module" [...])
# ##
# ##   # Boilerplate code, which pulls in the Zephyr build system.
# ##   cmake_minimum_required(VERSION 3.13.1)
# ##
# ##   # Project source files.
# ##   target_sources(app PRIVATE ../src/main.c)
# ##   target_sources(app PRIVATE ../lib/led/led.c)
# ##   target_sources(app PRIVATE ../lib/led/Button.c)
# ##
# ##   # -----------------------------------------------------------------
# ##   # PlatformIO
# ##   #
# ##   # CMakeLists.txt file enables features supported by Zephyr’s build system, e.g. board-specific kernel configuration files.
# ##   # A typical CMakeLists.txt file has the following content:
# ##   # -----------------------------------------------------------------
# ##
# ##   # Boilerplate code, which pulls in the Zephyr build system.
# ##   cmake_minimum_required(VERSION 3.13.1)
# ##   include($ENV{ZEPHYR_BASE}/cmake/app/boilerplate.cmake NO_POLICY_SCOPE)
# ##   project(my_zephyr_app)
# ##
# ##   # Add your source file to the "app" target. This must come after the boilerplate
# ##   # code, which defines the target. Note relative path to source file
# ##   target_sources(app PRIVATE ../src/main.c)
# ##
# ##   # -----------------------------------------------------------------
# ##   # examples\projects\zephyr
# ##   # -----------------------------------------------------------------
# ##   cmake_minimum_required(VERSION 3.13.1)
# ##   find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
# ##   project(luos_sample_on_zephyr)
# ##
# ##   target_sources(app PRIVATE src/main.c)
# ##   target_sources(app PRIVATE lib/led/led.c)
# ##   target_include_directories(app PRIVATE lib/led)
# ##
# ##   # -----------------------------------------------------------------
# ##   # zephyr
# ##   # -----------------------------------------------------------------
# ##   add_subdirectory_ifdef(CONFIG_LUOS ../network/robus/HAL/zephyr)
# ##   add_subdirectory_ifdef(CONFIG_LUOS ../engine/HAL/zephyr)
# ##
# ##   # -----------------------------------------------------------------
# ##   # engine\HAL\zephyr
# ##   # -----------------------------------------------------------------
# ##   if(CONFIG_LUOS)
# ##       zephyr_interface_library_named(LUOS_ENGINE)
# ##
# ##       zephyr_include_directories(
# ##           ../../../network/robus/inc
# ##           ../../../network/robus/zephyr
# ##           ../../../engine/HAL/zephyr
# ##           ../../../engine/core
# ##           ../../../engine/bootloader
# ##           ../../../engine/OD
# ##       )
# ##
# ##       zephyr_library()
# ##       ###   (
# ##           ../../../engine/core/src/luos_engine.c
# ##           ../../../engine/core/src/luos_utils.c
# ##           ../../../engine/core/src/profile_core.c
# ##           ../../../engine/core/src/routing_table.c
# ##           ../../../engine/core/src/streaming.c
# ##           ../../../engine/core/src/timestamp.c
# ##           ../../../engine/bootloader/bootloader_core.c
# ##           ../../../engine/HAL/zephyr/luos_hal.c
# ##       )
# ##
# ##       zephyr_library_link_libraries(LUOS_ENGINE)
# ##       target_link_libraries(LUOS_ENGINE INTERFACE zephyr_interface)
# ##   endif()
# ##
# ##   # -----------------------------------------------------------------
# ##   # network\robus\HAL\zephyr
# ##   # -----------------------------------------------------------------
# ##   if(CONFIG_LUOS)
# ##       zephyr_interface_library_named(LUOS_ROBUS)
# ##
# ##       zephyr_include_directories(
# ##           ../../inc
# ##           ../zephyr
# ##           ../../../../engine/HAL/zephyr
# ##       )
# ##
# ##       zephyr_library()
# ##       zephyr_library_sources(
# ##           ../../../src/msg_alloc.c
# ##           ../../../src/port_manager.c
# ##           ../../../src/reception.c
# ##           ../../../src/robus.c
# ##           ../../../src/topic.c
# ##           ../../../src/transmission.c
# ##           ../../../HAL/zephyr/robus_hal.c
# ##       )
# ##
# ##       zephyr_library_link_libraries(LUOS_ROBUS)
# ##       target_link_libraries(LUOS_ROBUS INTERFACE zephyr_interface)
# ##   endif()
