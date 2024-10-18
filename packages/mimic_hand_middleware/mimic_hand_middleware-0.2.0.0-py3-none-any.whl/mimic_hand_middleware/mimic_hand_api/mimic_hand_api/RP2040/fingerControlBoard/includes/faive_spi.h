#ifndef __FAIVE_SPI_H__
#define __FAIVE_SPI_H__

#include "pico/stdlib.h"
#include "hardware/spi.h"

#define LOW                 0
#define HIGH                1

#define SPI_BUS_SENSORS     0
#define SPI_BUS_MOTORS      1

#define spi0_miso_pin       16
#define spi0_sck_pin        18
#define spi0_mosi_pin       19

#define spi1_miso_pin       12
#define spi1_sck_pin        10
#define spi1_mosi_pin       11

#define SPI_MODE_0          0
#define SPI_MODE_1          1
#define SPI_MODE_2          2
#define SPI_MODE_3          3

void initSPI(uint8_t bus, uint32_t speed, uint8_t mode, spi_order_t order);
void SPI_write(uint8_t bus, uint8_t* data, uint8_t len);
void SPI_read(uint8_t bus, uint8_t* data, uint8_t len);
void SPI_write_read(uint8_t bus, uint8_t* writeData, uint8_t writeLen, uint8_t* readData, uint8_t readLen);

#endif // End of __FAIVE_SPI_H__ definition check