#ifndef __FAIVE_ADC_H__
#define __FAIVE_ADC_H__

#define FSR1                28
#define FSR2                27
#define FSR3                26

class faiveADC
{
    public:
        faiveADC();

        void read(float* outputPointer);
};

#endif // End of __FAIVE_ADC_H__ definition check