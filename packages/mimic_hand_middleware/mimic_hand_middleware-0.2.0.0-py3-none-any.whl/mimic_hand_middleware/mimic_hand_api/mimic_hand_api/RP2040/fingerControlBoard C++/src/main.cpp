#include "main.h"
#include <stdio.h>
#include "pico/stdlib.h"
#include "faive_spi.h"
#include "faive_uart.h"
#include "faive_adc.h"
#include "faive_lsm6dsm.h"
#include "faive_mlx90393.h"
#include "faive_as5045b.h"

// TODO: Add CSH1 once we have the new flexPCB version
const uint8_t chipSelector[] = {CSI1, CSI2, CSI3, CSH2, CSH3, CSH4};

void error_handler(void)
{
    gpio_put(LED_ERROR, 1);
    while(true)
    {

    }
}

int main() 
{
    bool status = true;

    // Variables to test flexPCB
    float dataFSR[3];
    float dataIMU[18];
    float dataHES[9];

    // Variables to test Communication
    char testCommunication[20];
    uint8_t len;
    char devices[] = {'0', '1', '2', '3', '4', '5'};

    // Variables to test Spool Sensing
    uint8_t nSensors = 3;
    float angles[nSensors];
    bool sensorStatus[nSensors];
    uint8_t CS = 7;

    stdio_init_all();

    // Configure Error LED
    gpio_init(LED_ERROR);
    gpio_set_dir(LED_ERROR, GPIO_OUT);
    gpio_put(LED_ERROR, LOW);

    gpio_init(CS);
    gpio_set_dir(CS, GPIO_OUT);
    gpio_put(CS, HIGH);
    gpio_set_drive_strength(CS, GPIO_DRIVE_STRENGTH_12MA);

    // Configure Chip Selects
    for (int i = 0; i < sizeof(chipSelector); i++)
    {
        gpio_init(chipSelector[i]);
        gpio_set_dir(chipSelector[i], GPIO_OUT);
        gpio_set_drive_strength(chipSelector[i], GPIO_DRIVE_STRENGTH_8MA);
        gpio_put(chipSelector[i], HIGH);
    }

    // Initialize Communication
    initUART();

    // Initialize ADC
    faiveADC ADC = faiveADC();

    // Initialize SPI1
    faiveSPI SPImotorBus = faiveSPI(SPI_BUS_MOTORS, 1000000, SPI_MODE_2, SPI_MSB_FIRST);
    faiveSPI SPIsensorBus = faiveSPI(SPI_BUS_SENSORS, 1000000, SPI_MODE_3, SPI_MSB_FIRST);

    // Initialize Spool Sensing
    faiveAS5045B spoolSensors = faiveAS5045B(SPImotorBus, CS, nSensors);

    // Initialize IMU & HES
    faiveLSM6DSM IMU = faiveLSM6DSM(SPIsensorBus);
    faiveMLX90393 HES = faiveMLX90393(SPIsensorBus);
    for (int i = 0; i < sizeof(chipSelector); i++)
    {
        if (i < 3)
        {
            status = IMU.init(chipSelector[i]);
        } else {
            status = HES.init(chipSelector[i]);
        }

        if (!status)
        {
            error_handler();
        }
    }

    while (true)
    {
        // // TEST ADC
        // ADC.read(dataFSR);
        // printf("FSR data: \t Proximal: %.2f \t Intermediate: %.2f \t Distal: %.2f \n\n", dataFSR[2], dataFSR[1], dataFSR[0]);
        // sleep_ms(500);

        // TEST flexPCB
        IMU.read(CSI1, dataIMU);
        IMU.read(CSI2, dataIMU+6);
        IMU.read(CSI3, dataIMU+12);

        HES.read(CSH2, dataHES);
        HES.read(CSH3, dataHES+3);
        HES.read(CSH4, dataHES+6);

        printf("Sensors on MCP:\n");
        printf("Accelerometer: \t X: %.2f \t Y: %.2f \t Z: %.2f \n", dataIMU[3], dataIMU[4], dataIMU[5]);
        printf("Gyroscope: \t X: %.2f \t Y: %.2f \t Z: %.2f \n", dataIMU[0], dataIMU[1], dataIMU[2]);
        printf("Hall Effect: \t X: %.2f \t Y: %.2f \t Z: %.2f \n\n", dataHES[0], dataHES[1], dataHES[2]);

        printf("Sensors on PIP:\n");
        printf("Accelerometer: \t X: %.2f \t Y: %.2f \t Z: %.2f \n", dataIMU[9], dataIMU[10], dataIMU[11]);
        printf("Gyroscope: \t X: %.2f \t Y: %.2f \t Z: %.2f \n", dataIMU[6], dataIMU[7], dataIMU[8]);
        printf("Hall Effect: \t X: %.2f \t Y: %.2f \t Z: %.2f \n\n", dataHES[3], dataHES[4], dataHES[5]);

        printf("Sensors on DIP:\n");
        printf("Accelerometer: \t X: %.2f \t Y: %.2f \t Z: %.2f \n", dataIMU[15], dataIMU[16], dataIMU[17]);
        printf("Gyroscope: \t X: %.2f \t Y: %.2f \t Z: %.2f \n", dataIMU[12], dataIMU[13], dataIMU[14]);
        printf("Hall Effect: \t X: %.2f \t Y: %.2f \t Z: %.2f \n\n", dataHES[6], dataHES[7], dataHES[8]);
        sleep_ms(100);
        
        // // TEST SPOOL SENSORS
        // spoolSensors.readSpoolAngles(angles, sensorStatus);

        // for (int i = 0; i < nSensors; i++)
        // {
        //     if (sensorStatus[i])
        //     {
        //         printf("\033[0;32m");
        //     } else {
        //         printf("\033[0;31m");
        //     }

        //     printf("Spool %d --> \t Angle: %.5f \n", i, angles[i]);
        //     printf("\033[1;0m");
        // }
        // printf("\n");
        // sleep_ms(100);
        
        // // TEST COMMUNICATION
        // sleep_ms(5000);
        // printf("Sending data in 5 sec...\n\n");
        // sleep_ms(5000);

        // len = sprintf(testCommunication, "This is a test");
        // for (int i = 0; i < sizeof(devices); i++)
        // {
        //     UART_write(devices[i], '0', testCommunication, len);
        //     sleep_ms(1000);
        // }
    }

    return 0;
}