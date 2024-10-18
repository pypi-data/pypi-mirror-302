#ifndef __AS5045B_H__
#define __AS5045B_H__

#include "pico/stdlib.h"
#include "faive_spi.h"

void readSensor(uint8_t CS, uint8_t nSensors, uint8_t* outputPointer);

void readSpoolAngles(uint8_t CS, uint8_t nSensors, float* outputPointer, uint8_t* statusPointer);

#endif // End of __AS5045B_H__ definition check