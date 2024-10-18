#include "faive_lsm6dsm.h"

faiveLSM6DSM::faiveLSM6DSM() : _spi(), _gyro_range(), _acc_range() {}

faiveLSM6DSM::faiveLSM6DSM(faiveSPI spi) : _spi(spi), _gyro_range(), _acc_range() {}

// Sets the SPI bus that is used
void faiveLSM6DSM::setSPIbus(faiveSPI spi)
{
    _spi = spi;
}

// Read mulitple 8-bit registers
void faiveLSM6DSM::readMultipleRegisters(uint8_t CS, uint8_t* outputPointer, uint8_t reg, uint8_t length)
{
    uint8_t cmd_buff[1];

    cmd_buff[0] = reg | 0x80;

    gpio_put(CS, LOW);
    
    // Send write command
    _spi.write(cmd_buff, sizeof(cmd_buff));

    // Read data
    _spi.read(outputPointer, length);

    gpio_put(CS, HIGH);
}

// Write multiple 8-bit registers
void faiveLSM6DSM::writeMultipleRegisters(uint8_t CS, uint8_t reg, uint8_t* data, uint8_t length)
{
    uint8_t cmd_buff[1];

    cmd_buff[0] = reg;

    gpio_put(CS, LOW);

    // Send write command
    _spi.write(cmd_buff, sizeof(cmd_buff));

    // Write data
    _spi.write(data, length);

    gpio_put(CS, HIGH);
}

// Convert raw sensor values to floats
float faiveLSM6DSM::calculate_gyro(uint16_t rawGyro)
{
    return ((float) twosComplement(rawGyro)) * 2 * _gyro_range / 0xFFFF;
}

float faiveLSM6DSM::calculate_acceleration(uint16_t rawAcceleration)
{
	return ((float) twosComplement(rawAcceleration)) * 2 * _acc_range / 0xFFFF;
}

int16_t faiveLSM6DSM::twosComplement(uint16_t input)
{
    int16_t output;

    output = (int16_t) input;
    if(input > 0x7FFF)
    {
        output -= 0x10000;
    }

    return output;
}

// IMU initialization
bool faiveLSM6DSM::init(uint8_t CS)
{
    uint8_t sanityCheck[4];
    uint8_t dataToWrite[4];
    uint8_t XL_FS;
    uint8_t G_FS;

    // Set Accelerometer and Gyro range
    XL_FS = XL_FS_2;
    G_FS = G_FS_250;

    switch (XL_FS)
    {
        case XL_FS_2:
            _acc_range = 2;
            break;

        case XL_FS_4:
            _acc_range = 4;
            break;

        case XL_FS_8:
            _acc_range = 8;
            break;

        case XL_FS_16:
            _acc_range = 16;
            break;
    }

    switch (XL_FS)
    {
        case G_FS_125:
            _gyro_range = 125;
            break;

        case G_FS_250:
            _gyro_range = 250;
            break;

        case G_FS_500:
            _gyro_range = 500;
            break;

        case G_FS_1000:
            _gyro_range = 1000;
            break;

        case G_FS_2000:
            _gyro_range = 2000;
            break;
    }

    // Write Registers
    dataToWrite[0] = XL_ODR_208 | XL_FS; // CTRL1_XL
    dataToWrite[1] = G_ODR_208 | G_FS; // CTRL2_G
    dataToWrite[2] = CTRL3_C_DEFAULT; // CTRL3_C
    dataToWrite[3] = CTRL4_C_DISABLE_I2C; // CTRL4_C

    writeMultipleRegisters(CS, CTRL1_XL, dataToWrite, sizeof(dataToWrite));

    sleep_ms(100);

    // Read registers after writing
    readMultipleRegisters(CS, sanityCheck, CTRL1_XL, sizeof(dataToWrite));

    if(sanityCheck[0] != dataToWrite[0] || sanityCheck[1] != dataToWrite[1] || sanityCheck[2] != dataToWrite[2] || sanityCheck[3] != dataToWrite[3])
    {
        return false;
    } else {
        return true;
    }
}

// Read Raw IMU Accelerometer and Gyroscope
void faiveLSM6DSM::read(uint8_t CS, float* outputPointer)
{
    uint8_t buffer[12];
    uint16_t tmp;

    readMultipleRegisters(CS, buffer, OUTX_L_G, sizeof(buffer));

    for(uint8_t i = 0; i < sizeof(buffer); i += 2)
    {
        tmp = ((uint16_t) buffer[i]) | (((uint16_t) buffer[i+1]) << 8);
        if(i < 5)
        {
            *outputPointer = calculate_gyro(tmp);
        } else {
            *outputPointer = calculate_acceleration(tmp);
        }
        outputPointer++;
    }
}

void faiveLSM6DSM::test(uint8_t CS, uint8_t* outputPointer)
{
    uint8_t whoAmI;

    readMultipleRegisters(CS, &whoAmI, WHO_AM_I, 1);

    *outputPointer = whoAmI;
}