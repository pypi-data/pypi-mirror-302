#ifndef __AS5045B_H__
#define __AS5045B_H__

#include "faive_spi.h"

class faiveAS5045B
{
    public:
        faiveAS5045B();

        faiveAS5045B(faiveSPI spi, uint8_t CS, uint8_t nSensors);

        void init(faiveSPI spi, uint8_t CS, uint8_t nSensors);

        void readSpoolAngles(float* angles, bool* sensorStatus);

    private:
        faiveSPI _spi;
        uint8_t _CS;
        uint8_t _nSensors;

        void readSensors(uint8_t* outputPointer, uint8_t len);
};

#endif // End of __AS5045B_H__ definition check