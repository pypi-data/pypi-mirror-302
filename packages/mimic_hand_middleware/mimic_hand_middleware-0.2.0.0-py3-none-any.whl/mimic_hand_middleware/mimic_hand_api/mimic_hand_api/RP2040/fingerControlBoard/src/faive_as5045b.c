#include "faive_as5045b.h"

void readSensor(uint8_t CS, uint8_t len, uint8_t* outputPointer)
{   
    gpio_put(CS, LOW);
    
    SPI_read(SPI_BUS_MOTORS, outputPointer, len);

    gpio_put(CS, HIGH);
}

void readSpoolAngles(uint8_t CS, uint8_t nSensors, float* outputPointer, uint8_t* statusPointer)
{
    uint8_t len = (19 * nSensors + 1) / 8 + 1;
    uint8_t n = len / 8 + 1;

    uint8_t rawData[len];
    uint64_t data[n];
    uint32_t spoolData[nSensors];
    uint16_t rawAngle;

    // Initialize arrays
    for (int i = 0; i < n; i++)
    {
        data[i] = 0;
    }

    for (int i = 0; i < nSensors; i++)
    {
        spoolData[i] = 0;
    }

    // Read Spool sensors
    readSensor(CS, len, rawData);

    // Fill data into large array
    for (int i = 0; i < len; i++)
    {
        data[i / 8] |= ((uint64_t) rawData[i]) << (8 * (7 - (i % 8)));
    }

    // Separate data from each spool into its own variable
    uint8_t ind = 1;
    int8_t diff = 0;
    for (int i = 0; i < nSensors; i++)
    {
        diff = 45 - (ind % 64);

        if (diff >= 0)
        {
            spoolData[i] = (uint32_t) ((data[ind / 64] >> diff) & 0x000000000007FFFF);
        } else {
            spoolData[i] = (uint32_t) (((data[ind / 64] << (-diff)) | (data[ind / 64 + 1] >> (diff + 64))) & 0x000000000007FFFF);
        }

        ind += 19;
    }

    // Calculate angle and status for each sensor
    for (int i = 0; i < nSensors; i++)
    {
        rawAngle = (uint16_t) ((spoolData[i] >> 7) & 0x00000FFF);
        *outputPointer = rawAngle * 360.0f / 4095.0f;
        outputPointer++;

        for (int j = 6; j > 0; j--)
        {
            *statusPointer = (uint8_t) ((spoolData[i] >> j) & 1);
            statusPointer++;
        }
    }
}

