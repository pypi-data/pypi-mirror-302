cmake_minimum_required(VERSION 3.12)

# Pull in SDK (must be before project)
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

include(pico_extras_import_optional.cmake)

project(faive-integration C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.3.0")
    message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.3.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

# Initialize the SDK
pico_sdk_init()

add_executable(app 
               src/main.c 
               src/faive_spi.c 
               src/faive_adc.c 
               src/faive_uart.c
               src/faive_lsm6dsm.c 
               src/faive_mlx90393.c 
               src/faive_as5045b.c
               )

target_include_directories(app PUBLIC includes)

# pull in common dependencies
target_link_libraries(app pico_stdlib hardware_spi hardware_adc hardware_uart)

# enable usb output, disable uart output
pico_enable_stdio_usb(app 1)
pico_enable_stdio_uart(app 0)

# create map/bin/hex file etc.
pico_add_extra_outputs(app)

add_compile_options(-Wall
        -Wno-format          # int != int32_t as far as the compiler is concerned because gcc has int32_t as long int
        -Wno-unused-function # we have some for the docs that aren't called
        -Wno-maybe-uninitialized
        )
