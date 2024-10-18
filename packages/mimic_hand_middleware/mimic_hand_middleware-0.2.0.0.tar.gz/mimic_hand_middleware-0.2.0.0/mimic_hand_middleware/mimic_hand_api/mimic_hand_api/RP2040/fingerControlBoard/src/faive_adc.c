#include "faive_adc.h"
#include "pico/stdlib.h"
#include "hardware/adc.h"

const float conversion_factor = 3.3f / (1 << 12);

void initADC(void)
{
    adc_init();
    adc_gpio_init(FSR1);
    adc_gpio_init(FSR2);
    adc_gpio_init(FSR3);
}

void readFSR(float* outputPointer)
{
    uint16_t result;

    for(int i = 0; i < 3; i++)
    {
        adc_select_input(i);
        result = adc_read();
        *outputPointer = ((float) result) * conversion_factor;
        outputPointer++;
    }
}

