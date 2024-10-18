#ifndef __LSM6DSM_H__
#define __LSM6DSM_H__

#include "pico/stdlib.h"
#include "faive_spi.h"

/************** Register Map **************/

// Embedded functions configuration register
#define FUNC_CFG_ACCESS                 0x01

// Sensor sync configuration registers
#define SENSOR_SYNC_TIME_FRAME          0x04 
#define SENSOR_SYNC_RES_RATIO           0x05

// FIFO configuration registers
#define FIFO_CTRL1                      0x06
#define FIFO_CTRL2                      0x07
#define FIFO_CTRL3                      0x08
#define FIFO_CTRL4                      0x09
#define FIFO_CTRL5                      0x0A

// DRDY Pulse configuration register
#define DRDY_PULSE_CFG                  0x0B

// Interrupt pin control
#define INT1_CTRL                       0x0D
#define INT2_CTRL                       0x0E

// Who I am ID (read only)
#define WHO_AM_I                        0x0F

// Accelerometer & Gyroscope control registers
#define CTRL1_XL                        0x10
#define CTRL2_G                         0x11
#define CTRL3_C                         0x12
#define CTRL4_C                         0x13
#define CTRL5_C                         0x14
#define CTRL6_C                         0x15
#define CTRL7_G                         0x16
#define CTRL8_XL                        0x17
#define CTRL9_XL                        0x18
#define CTRL10_C                        0x19

// I2C master configuration register
#define MASTER_CONFIG                   0x1A

// Interrupt registers (read only)
#define WAKE_UP_SRC                     0x1B
#define TAP_SRC                         0x1C
#define D6D_SRC                         0x1D

// Status data register for UI and OIS data (read only)
#define STATUS_REG                      0x1E

// Temperature output data registers (read only)
#define OUT_TEMP_L                      0x20
#define OUT_TEMP_H                      0x21

// Gyroscope output data registers (read only)
#define OUTX_L_G                        0x22
#define OUTX_H_G                        0x23
#define OUTY_L_G                        0x24
#define OUTY_H_G                        0x25
#define OUTZ_L_G                        0x26
#define OUTZ_H_G                        0x27

// Accelerometer output data registers (read only)
#define OUTX_L_XL                       0x28
#define OUTX_H_XL                       0x29
#define OUTY_L_XL                       0x2A
#define OUTY_H_XL                       0x2B
#define OUTZ_L_XL                       0x2C
#define OUTZ_H_XL                       0x2D

// Sensor hub output registers (read only)
#define SENSORHUB1_REG                  0x2E
#define SENSORHUB2_REG                  0x2F
#define SENSORHUB3_REG                  0x30
#define SENSORHUB4_REG                  0x31
#define SENSORHUB5_REG                  0x32
#define SENSORHUB6_REG                  0x33
#define SENSORHUB7_REG                  0x34
#define SENSORHUB8_REG                  0x35
#define SENSORHUB9_REG                  0x36
#define SENSORHUB10_REG                 0x37
#define SENSORHUB11_REG                 0x38
#define SENSORHUB12_REG                 0x39

// FIFO status registers (read only)
#define FIFO_STATUS1                    0x3A
#define FIFO_STATUS2                    0x3B
#define FIFO_STATUS3                    0x3C
#define FIFO_STATUS4                    0x3D

// FIFO data output registers (read only)
#define FIFO_DATA_OUT_L                 0x3E
#define FIFO_DATA_OUT_H                 0x3F

// Timestamp output registers
#define TIMESTAMP0_REG                  0x40  // read only
#define TIMESTAMP1_REG                  0x41  // read only
#define TIMESTAMP2_REG                  0x42

// Step counter registers (read only)
#define STEP_TIMESTAMP_L                0x49
#define STEP_TIMESTAMP_H                0x4A
#define STEP_COUNTER_L                  0x4B
#define STEP_COUNTER_H                  0x4C

// more Sensor hub output registers (read only)
#define SENSORHUB13_REG                 0x4D
#define SENSORHUB14_REG                 0x4E
#define SENSORHUB15_REG                 0x4F
#define SENSORHUB16_REG                 0x50
#define SENSORHUB17_REG                 0x51
#define SENSORHUB18_REG                 0x52

// more Interrupt registers
#define FUNC_SRC1                       0x53 // read only
#define FUNC_SRC2                       0x54 // read only
#define WRIST_TILT_IA                   0x55 // read only
#define TAP_CFG                         0x58
#define TAP_THS_6D                      0x59
#define INT_DUR2                        0x5A
#define WAKE_UP_THS                     0x5B
#define WAKE_UP_DUR                     0x5C
#define FREE_FALL                       0x5D
#define MD1_CFG                         0x5E
#define MD2_CFG                         0x5F

// Master command code
#define MASTER_CMD_CODE                 0x60

// Sensor sync SPI error code
#define SENS_SYNC_SPI_ERROR_CODE        0x61

// External magnetometer raw data output registers (read only)
#define OUT_MAG_RAW_X_L                 0x66
#define OUT_MAG_RAW_X_H                 0x67
#define OUT_MAG_RAW_Y_L                 0x68
#define OUT_MAG_RAW_Y_H                 0x69
#define OUT_MAG_RAW_Z_L                 0x6A
#define OUT_MAG_RAW_Z_H                 0x6B

// OIS connection registers
#define INT_OIS                         0x6F
#define CTRL1_OIS                       0x70
#define CTRL2_OIS                       0x71
#define CTRL3_OIS                       0x72

// Accelerometer user offset correction
#define X_OFS_USR                       0x73
#define Y_OFS_USR                       0x74
#define Z_OFS_USR                       0x75

/********** End of Register Map ***********/


/********* Basic Register Values **********/

// CTRL1_XL Register
#define XL_ODR_OFF                      0x00
#define XL_ODR_12p5                     0x10
#define XL_ODR_26                       0x20
#define XL_ODR_52                       0x30
#define XL_ODR_104                      0x40
#define XL_ODR_208                      0x50
#define XL_ODR_416                      0x60
#define XL_ODR_833                      0x70
#define XL_ODR_1666                     0x80
#define XL_ODR_3333                     0x90
#define XL_ODR_6666                     0xA0

#define XL_FS_2                         0x00
#define XL_FS_16                        0x04
#define XL_FS_4                         0x08
#define XL_FS_8                         0x0C

#define XL_LPF1_BW_ODR_HALF             0x00
#define XL_LPF1_BW_ODR_QUARTER          0x02

#define XL_ANALOG_LPF_BW_1500           0x00
#define XL_ANALOG_LPF_BW_400            0x01

// CTRL2_G Register
#define G_ODR_OFF                       0x00
#define G_ODR_12p5                      0x10
#define G_ODR_26                        0x20
#define G_ODR_52                        0x30
#define G_ODR_104                       0x40
#define G_ODR_208                       0x50
#define G_ODR_416                       0x60
#define G_ODR_833                       0x70
#define G_ODR_1666                      0x80
#define G_ODR_3333                      0x90
#define G_ODR_6666                      0xA0

#define G_FS_250                        0x00
#define G_FS_500                        0x04
#define G_FS_1000                       0x08
#define G_FS_2000                       0x0C
#define G_FS_125                        0x02

// CTRL3_G Register
#define CTRL3_C_DEFAULT                 0x04

// CTRL4_C Register
#define CTRL4_C_DISABLE_I2C             0x04
#define CTRL4_C_ENABLE_G_LPF1           0x02

// FIFO_CTRL1 Register
#define FIFO_TH

// FIFO_CTRL3 Register
#define FIFO_G_DISABLED                 0x00
#define FIFO_G_DECIMATION_1             0x08
#define FIFO_G_DECIMATION_2             0x10
#define FIFO_G_DECIMATION_3             0x18
#define FIFO_G_DECIMATION_4             0x20
#define FIFO_G_DECIMATION_8             0x28
#define FIFO_G_DECIMATION_16            0x30
#define FIFO_G_DECIMATION_32            0x38
#define FIFO_XL_DISABLED                0x00
#define FIFO_XL_DECIMATION_1            0x01
#define FIFO_XL_DECIMATION_2            0x02
#define FIFO_XL_DECIMATION_3            0x03
#define FIFO_XL_DECIMATION_4            0x04
#define FIFO_XL_DECIMATION_8            0x05
#define FIFO_XL_DECIMATION_16           0x06
#define FIFO_XL_DECIMATION_32           0x07

// FIFO_CTRL5 Register
#define FIFO_ODR_OFF                    0x00
#define FIFO_ODR_12p5                   0x08
#define FIFO_ODR_26                     0x10
#define FIFO_ODR_52                     0x18
#define FIFO_ODR_104                    0x20
#define FIFO_ODR_208                    0x28
#define FIFO_ODR_416                    0x30
#define FIFO_ODR_833                    0x38
#define FIFO_ODR_1666                   0x40
#define FIFO_ODR_3333                   0x48
#define FIFO_ODR_6666                   0x50

#define FIFO_MODE_BYPASS                0x00
#define FIFO_MODE_FIFO                  0x01
#define FIFO_MODE_CONTINUOUS2FIFO       0x03
#define FIFO_MODE_BYPASS2CONTINUOUS     0x04
#define FIFO_MODE_CONTINUOUS            0x06
/******************************************/

// Read multiple 8-bit registers
static void readMultipleRegisters(uint8_t CS, uint8_t* outputPointer, uint8_t reg, uint8_t length);

// Write multiple 8-bit registers
static void writeMultipleRegisters(uint8_t CS, uint8_t reg, uint8_t* data, uint8_t length);

// Convert Raw ADC value to dps
static float calculate_gyro(uint16_t raw_Gyro);

// Convert Raw ADC value to g
static float calculate_acceleration(uint16_t rawAcceleration);

// Calculate the twos complement of an unisgned 16-bit integer
static int16_t twosComplement(uint16_t input);
        
// Initialise IMU by cinfiguring Registers
bool initIMU(uint8_t CS);

// Read IMU Accelerometer and Gyroscope
void readIMU(uint8_t CS, float* outputPointer);

static uint16_t readRawTemp(uint8_t CS);

float readTempC(uint8_t CS);

void testIMU(uint8_t CS, uint8_t* outputPointer);

#endif // End of __LSM6DSM_H__ definition check