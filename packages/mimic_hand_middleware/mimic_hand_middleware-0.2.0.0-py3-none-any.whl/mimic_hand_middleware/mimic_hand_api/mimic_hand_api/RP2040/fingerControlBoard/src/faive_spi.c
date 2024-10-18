#include "faive_spi.h"

spi_inst_t *SPI_0 = spi0;
spi_inst_t *SPI_1 = spi1;

void initSPI(uint8_t bus, uint32_t speed, uint8_t mode, spi_order_t order)
{
    spi_cpol_t cpol;
    spi_cpha_t cpha;

    switch (mode)
    {
        case SPI_MODE_0:
            cpol = SPI_CPOL_0;
            cpha = SPI_CPHA_0;
            break;

        case SPI_MODE_1:
            cpol = SPI_CPOL_0;
            cpha = SPI_CPHA_1;
            break;

        case SPI_MODE_2:
            cpol = SPI_CPOL_1;
            cpha = SPI_CPHA_0;
            break;

        case SPI_MODE_3:
            cpol = SPI_CPOL_1;
            cpha = SPI_CPHA_1;
            break;
        
        default:
            break;
    }

    switch (bus)
    {
        case SPI_BUS_SENSORS:
            spi_init(SPI_0, speed);
            
            spi_set_format(spi0, 8, cpol, cpha, order);

            gpio_set_function(spi0_sck_pin, GPIO_FUNC_SPI);
            gpio_set_function(spi0_miso_pin, GPIO_FUNC_SPI);
            gpio_set_function(spi0_mosi_pin, GPIO_FUNC_SPI);
            break;

        case SPI_BUS_MOTORS:
            spi_init(SPI_1, speed);
            
            spi_set_format(spi1, 8, cpol, cpha, order);

            gpio_set_function(spi1_sck_pin, GPIO_FUNC_SPI);
            gpio_set_function(spi1_miso_pin, GPIO_FUNC_SPI);
            gpio_set_function(spi1_mosi_pin, GPIO_FUNC_SPI);
            break;
        
        default:
            break;
    }
}

void SPI_read(uint8_t bus, uint8_t* data, uint8_t len)
{
    switch (bus)
    {
        case SPI_BUS_SENSORS:
            spi_read_blocking(SPI_0, 0, data, len);
            break;

        case SPI_BUS_MOTORS:
            spi_read_blocking(SPI_1, 0, data, len);
            break;
    }
}

void SPI_write(uint8_t bus, uint8_t* data, uint8_t len)
{
    switch (bus)
    {
        case SPI_BUS_SENSORS:
            spi_write_blocking(SPI_0, data, len);
            break;

        case SPI_BUS_MOTORS:
            spi_write_blocking(SPI_1, data, len);
            break;
    }
}

void SPI_write_read(uint8_t bus, uint8_t* writeData, uint8_t writeLen, uint8_t* readData, uint8_t readLen)
{
    uint8_t srcBuffer[writeLen + readLen];
    uint8_t dstBuffer[writeLen + readLen];

    for (int i = 0; i < writeLen; i++)
    {
        srcBuffer[i] = writeData[i];
    }

    switch (bus)
    {
        case SPI_BUS_SENSORS:
            spi_write_read_blocking(SPI_0, srcBuffer, dstBuffer, writeLen+readLen);
            break;

        case SPI_BUS_MOTORS:
            spi_write_read_blocking(SPI_1, srcBuffer, dstBuffer, writeLen+readLen);
            break;
    }

    for (int i = 0; i < readLen; i++)
    {
        readData[i] = dstBuffer[writeLen + i];
    }
}