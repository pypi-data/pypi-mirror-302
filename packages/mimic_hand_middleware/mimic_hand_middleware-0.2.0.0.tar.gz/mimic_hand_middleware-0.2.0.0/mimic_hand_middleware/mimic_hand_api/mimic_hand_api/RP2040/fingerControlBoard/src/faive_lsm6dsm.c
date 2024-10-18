#include "faive_lsm6dsm.h"
#include <stdio.h>

float gyro_range;
float acc_range;

// Read mulitple 8-bit registers
static void readMultipleRegisters(uint8_t CS, uint8_t* outputPointer, uint8_t reg, uint8_t length)
{
    uint8_t cmd_buff[1];

    cmd_buff[0] = reg | 0x80;

    gpio_put(CS, LOW);
    
    // Send write command
    SPI_write(SPI_BUS_SENSORS, cmd_buff, sizeof(cmd_buff));

    // Read data
    SPI_read(SPI_BUS_SENSORS, outputPointer, length);

    gpio_put(CS, HIGH);
}

// Write multiple 8-bit registers
static void writeMultipleRegisters(uint8_t CS, uint8_t reg, uint8_t* data, uint8_t length)
{
    uint8_t cmd_buff[1];

    cmd_buff[0] = reg;

    gpio_put(CS, LOW);

    // Send write command
    SPI_write(SPI_BUS_SENSORS, cmd_buff, sizeof(cmd_buff));

    // Write data
    SPI_write(SPI_BUS_SENSORS, data, length);

    gpio_put(CS, HIGH);
}

// Convert raw sensor values to floats
static float calculate_gyro(uint16_t rawGyro)
{
    return ((float) twosComplement(rawGyro)) * 2 * gyro_range / 0xFFFF;
}

static float calculate_acceleration(uint16_t rawAcceleration)
{
	return ((float) twosComplement(rawAcceleration)) * 2 * acc_range / 0xFFFF;
}

static int16_t twosComplement(uint16_t input)
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
bool initIMU(uint8_t CS)
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
            acc_range = 2;
            break;

        case XL_FS_4:
            acc_range = 4;
            break;

        case XL_FS_8:
            acc_range = 8;
            break;

        case XL_FS_16:
            acc_range = 16;
            break;
    }

    switch (XL_FS)
    {
        case G_FS_125:
            gyro_range = 125;
            break;

        case G_FS_250:
            gyro_range = 250;
            break;

        case G_FS_500:
            gyro_range = 500;
            break;

        case G_FS_1000:
            gyro_range = 1000;
            break;

        case G_FS_2000:
            gyro_range = 2000;
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
        printf("Error Initializing IMU :(\n");
        printf("CTRL1 Should be %X, but is %X \n", dataToWrite[0], sanityCheck[0]);
        printf("CTRL2 Should be %X, but is %X \n", dataToWrite[1], sanityCheck[1]);
        printf("CTRL3 Should be %X, but is %X \n", dataToWrite[2], sanityCheck[2]);
        printf("CTRL4 Should be %X, but is %X \n\n", dataToWrite[3], sanityCheck[3]);
        return false;
    } else {
        printf(" Initializing IMU Successful :)\n");
        printf("CTRL1 is %X \n", sanityCheck[0]);
        printf("CTRL2 is %X \n", sanityCheck[1]);
        printf("CTRL3 is %X \n", sanityCheck[2]);
        printf("CTRL4 is %X \n\n", sanityCheck[3]);
        return true;
    }
}

// Read Raw IMU Accelerometer and Gyroscope
void readIMU(uint8_t CS, float* outputPointer)
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

// Read Temperature
static uint16_t readRawTemp(uint8_t CS)
{
    uint8_t output[2];
    readMultipleRegisters(CS, output, OUT_TEMP_L, 2);
    return ((uint16_t) output[0]) | (((uint16_t) output[1]) << 8);
}

float readTempC(uint8_t CS)
{
    int16_t rawValue;
    float floatValue;

    rawValue = twosComplement(readRawTemp(CS));

    floatValue = ((float) rawValue) / 256;
    floatValue += 25;

    return floatValue;
}


void testIMU(uint8_t CS, uint8_t* outputPointer)
{
    uint8_t whoAmI;

    readMultipleRegisters(CS, &whoAmI, WHO_AM_I, 1);

    *outputPointer = whoAmI;
}