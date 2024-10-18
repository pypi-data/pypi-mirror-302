#include "faive_as5045b.h"

faiveAS5045B::faiveAS5045B() : _spi(), _CS(), _nSensors() {}

faiveAS5045B::faiveAS5045B(faiveSPI spi, uint8_t CS, uint8_t nSensors) : _spi(spi), _CS(CS), _nSensors(nSensors) {}

void faiveAS5045B::init(faiveSPI spi, uint8_t CS, uint8_t nSensors)
{
    _spi = spi;
    _CS = CS;
    _nSensors = nSensors;
}

void faiveAS5045B::readSensors(uint8_t* outputPointer, uint8_t len)
{   
    gpio_put(_CS, LOW);
    
    _spi.read(outputPointer, len);

    gpio_put(_CS, HIGH);
}

void faiveAS5045B::readSpoolAngles(float* angles, bool* sensorStatus)
{   
    uint8_t len = (19 * _nSensors + 1) / 8 + 1;
    uint8_t n = len / 8 + 1;

    uint8_t rawData[len];
    uint64_t data[n];
    uint32_t spoolData[_nSensors];
    uint16_t rawAngle;

    // Initialize arrays
    for (int i = 0; i < n; i++)
    {
        data[i] = 0;
    }

    for (int i = 0; i < _nSensors; i++)
    {
        spoolData[i] = 0;
    }

    // Read Spool sensors
    readSensors(rawData, len);

    // Fill data into large array
    for (int i = 0; i < len; i++)
    {
        data[i / 8] |= ((uint64_t) rawData[i]) << (8 * (7 - (i % 8)));
    }

    // Separate data from each spool into its own variable
    uint8_t ind = 1;
    int8_t diff = 0;
    for (int i = 0; i < _nSensors; i++)
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
    for (int i = 0; i < _nSensors; i++)
    {
        rawAngle = (uint16_t) ((spoolData[i] >> 7) & 0x00000FFF);
        *angles = rawAngle * 360.0f / 4095.0f;
        angles++;

        if (((spoolData[i] >> 2) & 0x0000001F) != 0x00000010)
        {
            *sensorStatus = false;
        } else {
            *sensorStatus = true;
        }
        sensorStatus++;
    }
}

