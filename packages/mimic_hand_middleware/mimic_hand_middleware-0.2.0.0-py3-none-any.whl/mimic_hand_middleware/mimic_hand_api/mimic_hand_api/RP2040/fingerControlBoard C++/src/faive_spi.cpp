#include "faive_spi.h"

faiveSPI::faiveSPI() : _bus(), _speed(), _mode(), _order() {}

faiveSPI::faiveSPI(uint8_t bus, uint32_t speed, uint8_t mode, spi_order_t order)
{
    init(bus, speed, mode, order);
}

void faiveSPI::init(uint8_t bus, uint32_t speed, uint8_t mode, spi_order_t order)
{
    _bus = bus;
    _speed = speed;
    _mode = mode;
    _order = order;

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
            _SPI = spi0;

            spi_init(_SPI, speed);
            
            spi_set_format(_SPI, 8, cpol, cpha, order);

            gpio_set_function(spi0_sck_pin, GPIO_FUNC_SPI);
            gpio_set_function(spi0_miso_pin, GPIO_FUNC_SPI);
            gpio_set_function(spi0_mosi_pin, GPIO_FUNC_SPI);
            break;

        case SPI_BUS_MOTORS:
            _SPI = spi1;
            spi_init(_SPI, speed);
            
            spi_set_format(_SPI, 8, cpol, cpha, order);

            gpio_set_function(spi1_sck_pin, GPIO_FUNC_SPI);
            gpio_set_function(spi1_miso_pin, GPIO_FUNC_SPI);
            gpio_set_function(spi1_mosi_pin, GPIO_FUNC_SPI);
            break;
        
        default:
            break;
    }
}

void faiveSPI::read(uint8_t* data, uint8_t len)
{
    spi_read_blocking(_SPI, 0, data, len);
}

void faiveSPI::write(uint8_t* data, uint8_t len)
{
    spi_write_blocking(_SPI, data, len);
}

void faiveSPI::write_read(uint8_t* writeData, uint8_t writeLen, uint8_t* readData, uint8_t readLen)
{
    uint8_t srcBuffer[writeLen + readLen];
    uint8_t dstBuffer[writeLen + readLen];

    for (int i = 0; i < writeLen; i++)
    {
        srcBuffer[i] = writeData[i];
    }

    spi_write_read_blocking(_SPI, srcBuffer, dstBuffer, writeLen+readLen);

    for (int i = 0; i < readLen; i++)
    {
        readData[i] = dstBuffer[writeLen + i];
    }
}