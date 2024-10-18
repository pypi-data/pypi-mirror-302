/*************************************************************
Adafruit MLX90393 Library adapted for use with the Faive hand
*************************************************************/
#include "faive_mlx90393.h"

/** Lookup table to convert raw values to uT based on [HALLCONF][GAIN_SEL][RES].
 */
const float mlx90393_lsb_lookup[2][8][4][2] = {

    /* HALLCONF = 0xC (default) */
    {
        /* GAIN_SEL = 0, 5x gain */
        {{0.751, 1.210}, {1.502, 2.420}, {3.004, 4.840}, {6.009, 9.680}},
        /* GAIN_SEL = 1, 4x gain */
        {{0.601, 0.968}, {1.202, 1.936}, {2.403, 3.872}, {4.840, 7.744}},
        /* GAIN_SEL = 2, 3x gain */
        {{0.451, 0.726}, {0.901, 1.452}, {1.803, 2.904}, {3.605, 5.808}},
        /* GAIN_SEL = 3, 2.5x gain */
        {{0.376, 0.605}, {0.751, 1.210}, {1.502, 2.420}, {3.004, 4.840}},
        /* GAIN_SEL = 4, 2x gain */
        {{0.300, 0.484}, {0.601, 0.968}, {1.202, 1.936}, {2.403, 3.872}},
        /* GAIN_SEL = 5, 1.667x gain */
        {{0.250, 0.403}, {0.501, 0.807}, {1.001, 1.613}, {2.003, 3.227}},
        /* GAIN_SEL = 6, 1.333x gain */
        {{0.200, 0.323}, {0.401, 0.645}, {0.801, 1.291}, {1.602, 2.581}},
        /* GAIN_SEL = 7, 1x gain */
        {{0.150, 0.242}, {0.300, 0.484}, {0.601, 0.968}, {1.202, 1.936}},
    },

    /* HALLCONF = 0x0 */
    {
        /* GAIN_SEL = 0, 5x gain */
        {{0.787, 1.267}, {1.573, 2.534}, {3.146, 5.068}, {6.292, 10.137}},
        /* GAIN_SEL = 1, 4x gain */
        {{0.629, 1.014}, {1.258, 2.027}, {2.517, 4.055}, {5.034, 8.109}},
        /* GAIN_SEL = 2, 3x gain */
        {{0.472, 0.760}, {0.944, 1.521}, {1.888, 3.041}, {3.775, 6.082}},
        /* GAIN_SEL = 3, 2.5x gain */
        {{0.393, 0.634}, {0.787, 1.267}, {1.573, 2.534}, {3.146, 5.068}},
        /* GAIN_SEL = 4, 2x gain */
        {{0.315, 0.507}, {0.629, 1.014}, {1.258, 2.027}, {2.517, 4.055}},
        /* GAIN_SEL = 5, 1.667x gain */
        {{0.262, 0.422}, {0.524, 0.845}, {1.049, 1.689}, {2.097, 3.379}},
        /* GAIN_SEL = 6, 1.333x gain */
        {{0.210, 0.338}, {0.419, 0.676}, {0.839, 1.352}, {1.678, 2.703}},
        /* GAIN_SEL = 7, 1x gain */
        {{0.157, 0.253}, {0.315, 0.507}, {0.629, 1.014}, {1.258, 2.027}},
    }};

/** Lookup table for conversion time based on [DIF_FILT][OSR].
 */
const float mlx90393_tconv[8][4] = {
    /* DIG_FILT = 0 */
    {1.27, 1.84, 3.00, 5.30},
    /* DIG_FILT = 1 */
    {1.46, 2.23, 3.76, 6.84},
    /* DIG_FILT = 2 */
    {1.84, 3.00, 5.30, 9.91},
    /* DIG_FILT = 3 */
    {2.61, 4.53, 8.37, 16.05},
    /* DIG_FILT = 4 */
    {4.15, 7.60, 14.52, 28.34},
    /* DIG_FILT = 5 */
    {7.22, 13.75, 26.80, 52.92},
    /* DIG_FILT = 6 */
    {13.36, 26.04, 51.38, 102.07},
    /* DIF_FILT = 7 */
    {25.65, 50.61, 100.53, 200.37},
};

faiveMLX90393::faiveMLX90393() : _spi(), _gain(), _osr(), _res_x(), _res_y(), _res_z(), _dig_filt() {}

faiveMLX90393::faiveMLX90393(faiveSPI spi) : _spi(spi), _gain(), _osr(), _res_x(), _res_y(), _res_z(), _dig_filt() {}

void faiveMLX90393::write_then_read(uint8_t CS, uint8_t *write_buffer, size_t write_len, uint8_t *read_buffer, size_t read_len)
{
  gpio_put(CS, LOW);

  // Write
  _spi.write(write_buffer, write_len);

  // Read
  _spi.read(read_buffer, read_len);

  gpio_put(CS, HIGH);
}

uint8_t faiveMLX90393::transceive(uint8_t CS, uint8_t *txbuf, uint8_t txlen, uint8_t *rxbuf, uint8_t rxlen, uint8_t interdelay)
{
  uint8_t status = 0;
  uint8_t i;
  uint8_t rxbuf2[rxlen + 2];

  write_then_read(CS, txbuf, txlen, rxbuf2, rxlen + 1);

  status = rxbuf2[0];
    
  for (i = 0; i < rxlen; i++)
  {
    rxbuf[i] = rxbuf2[i + 1];
  }

  sleep_ms(interdelay);

  return (status >> 2);
}

bool faiveMLX90393::writeRegister(uint8_t CS, uint8_t reg, uint16_t data)
{
  uint8_t tx[4] = {MLX90393_REG_WR, (uint8_t)(data >> 8), (uint8_t)(data & 0xFF), (uint8_t)(reg << 2)};
  return (transceive(CS, tx, sizeof(tx), NULL, 0, 0) == MLX90393_STATUS_OK);
}

bool faiveMLX90393::readRegister(uint8_t CS, uint8_t reg, uint16_t *data)
{
  uint8_t tx[2] = {MLX90393_REG_RR, (uint8_t)(reg << 2)};

  uint8_t rx[2];

  if (transceive(CS, tx, sizeof(tx), rx, sizeof(rx), 0) != MLX90393_STATUS_OK)
    return false;

  *data = ((uint16_t)rx[0] << 8) | rx[1];

  return true;
}

bool faiveMLX90393::exitMode(uint8_t CS)
{
  uint8_t tx[1] = {MLX90393_REG_EX};
  return (transceive(CS, tx, sizeof(tx), NULL, 0, 0) == MLX90393_STATUS_OK);
}

bool faiveMLX90393::reset(uint8_t CS)
{
  uint8_t tx[1] = {MLX90393_REG_RT};
  return (transceive(CS, tx, sizeof(tx), NULL, 0, 5) == MLX90393_STATUS_RESET);
}

bool faiveMLX90393::setTrigInt(uint8_t CS, bool state)
{
  uint16_t data = 0;
  readRegister(CS, MLX90393_CONF2, &data);

  // mask off trigint bit
  data &= ~0x8000;

  // set trigint bit if desired
  if (state)
  {
    /* Set the INT, highest bit */
    data |= 0x8000;
  }

  return writeRegister(CS, MLX90393_CONF2, data);
}

bool faiveMLX90393::setGain(uint8_t CS, mlx90393_gain_t gain)
{
  _gain = gain;

  uint16_t data = 0;
  readRegister(CS, MLX90393_CONF1, &data);

  // mask off gain bits
  data &= ~0x0070;

  // set gain bits
  data |= gain << MLX90393_GAIN_SHIFT;

  return writeRegister(CS, MLX90393_CONF1, data);
}

mlx90393_gain_t faiveMLX90393::getGain(void)
{
  return _gain;
}

bool faiveMLX90393::setResolution(uint8_t CS, mlx90393_axis_t axis, mlx90393_resolution_t resolution)
{
  uint16_t data = 0;
  readRegister(CS, MLX90393_CONF3, &data);

  switch (axis) 
  {
    case MLX90393_X:
      _res_x = resolution;
      data &= ~0x0060;
      data |= resolution << 5;
      break;
    case MLX90393_Y:
      _res_y = resolution;
      data &= ~0x0180;
      data |= resolution << 7;
      break;
    case MLX90393_Z:
      _res_z = resolution;
      data &= ~0x0600;
      data |= resolution << 9;
      break;
  }

  return writeRegister(CS, MLX90393_CONF3, data);
}

mlx90393_resolution_t faiveMLX90393::getResolution(mlx90393_axis_t axis)
{
  switch (axis)
  {
    case MLX90393_X:
      return _res_x;
    case MLX90393_Y:
      return _res_y;
    case MLX90393_Z:
      return _res_z;
  }
  // shouldn't get here, but to make compiler happy...
  return _res_x;
}

bool faiveMLX90393::setFilter(uint8_t CS, mlx90393_filter_t filter)
{
  _dig_filt = filter;

  uint16_t data = 0;
  readRegister(CS, MLX90393_CONF3, &data);

  data &= ~0x1C;
  data |= filter << 2;

  return writeRegister(CS, MLX90393_CONF3, data);
}

mlx90393_filter_t faiveMLX90393::getFilter(void)
{
  return _dig_filt;
}

bool faiveMLX90393::setOversampling(uint8_t CS, mlx90393_oversampling_t oversampling)
{
  _osr = oversampling;

  uint16_t data = 0;
  readRegister(CS, MLX90393_CONF3, &data);

  data &= ~0x03;
  data |= oversampling;

  return writeRegister(CS, MLX90393_CONF3, data);
}

mlx90393_oversampling_t faiveMLX90393::getOversampling(void)
{
  return _osr;
}

bool faiveMLX90393::startSingleMeasurement(uint8_t CS)
{
  uint8_t tx[1] = {MLX90393_REG_SM | MLX90393_AXIS_ALL};

  /* Set the device to single measurement mode */
  uint8_t stat = transceive(CS, tx, sizeof(tx), NULL, 0, 0);

  if ((stat == MLX90393_STATUS_OK) || (stat == MLX90393_STATUS_SMMODE))
  {
    return true;
  }
  return false;
}

bool faiveMLX90393::readMeasurement(uint8_t CS, float* outputPointer)
{
  uint8_t tx[1] = {MLX90393_REG_RM | MLX90393_AXIS_ALL};
  uint8_t rx[6] = {0};

  /* Read a single data sample. */
  if (transceive(CS, tx, sizeof(tx), rx, sizeof(rx), 0) != MLX90393_STATUS_OK) 
    return false;

  int16_t xi, yi, zi;

  /* Convert data to uT and float. */
  xi = (rx[0] << 8) | rx[1];
  yi = (rx[2] << 8) | rx[3];
  zi = (rx[4] << 8) | rx[5];

  if (_res_x == MLX90393_RES_18)
    xi -= 0x8000;
  if (_res_x == MLX90393_RES_19)
    xi -= 0x4000;
  if (_res_y == MLX90393_RES_18)
    yi -= 0x8000;
  if (_res_y == MLX90393_RES_19)
    yi -= 0x4000;
  if (_res_z == MLX90393_RES_18)
    zi -= 0x8000;
  if (_res_z == MLX90393_RES_19)
    zi -= 0x4000;
  
  *outputPointer = (float)xi * mlx90393_lsb_lookup[0][_gain][_res_x][0];
  *(outputPointer+1) = (float)yi * mlx90393_lsb_lookup[0][_gain][_res_y][0];
  *(outputPointer+2) = (float)zi * mlx90393_lsb_lookup[0][_gain][_res_z][1];

  return true;
}

float faiveMLX90393::dotProduct(const float vec1[3], const float vec2[3])
{
  return vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2];
}

void faiveMLX90393::crossProduct(const float vec1[3], const float vec2[3], float resVec[3])
{
  resVec[0] = vec1[1]*vec2[2]-vec1[2]*vec2[1];
  resVec[1] = vec1[2]*vec2[0]-vec1[0]*vec2[2];
  resVec[2] = vec1[0]*vec2[1]-vec1[1]*vec2[0];
}

float faiveMLX90393::VecLength(const float vec[3])
{
  return sqrt(vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2]);
}

float faiveMLX90393::angleVecToVecDIR(const float vec1[3], const float vec2[3], const float planeNorm[3])
{
  float angle = acos(dotProduct(vec1, vec2)/(VecLength(vec1)*VecLength(vec2)))*180/M_PI;
  float crossVec[3];
  crossProduct(vec1, vec2, crossVec);
  if (dotProduct(crossVec, planeNorm) > 0) 
    return 360-angle;
  else
    return angle;
}

bool faiveMLX90393::init(uint8_t CS)
{
  uint16_t sanityCheck[2];

  // Perform an Exit Mode operation
  exitMode(CS);

  // Perform a Soft reset
  reset(CS);

  // set INT pin to output interrupt
  setTrigInt(CS, false);

  sleep_ms(100);

  // Set Gain
  setGain(CS, MLX90393_GAIN_2X);

  // // Set resolution, per axis
  setResolution(CS, MLX90393_X, MLX90393_RES_18);
  setResolution(CS, MLX90393_Y, MLX90393_RES_18);
  setResolution(CS, MLX90393_Z, MLX90393_RES_18);

  // Set oversampling
  setOversampling(CS, MLX90393_OSR_2);

  // Set digital filtering
  setFilter(CS, MLX90393_FILTER_1);

  // Sanity Check
  readRegister(CS, MLX90393_CONF1, sanityCheck);
  readRegister(CS, MLX90393_CONF3, sanityCheck+1);

  if(sanityCheck[0] != 0x004C || sanityCheck[1] != 0x0546)
  {
    return false;
  }

  return true;
}

bool faiveMLX90393::read(uint8_t CS, float* outputPointer)
{
  if (!startSingleMeasurement(CS))
    return false;

  sleep_ms(mlx90393_tconv[_dig_filt][_osr] + 10);
  return readMeasurement(CS, outputPointer);
}

void faiveMLX90393::test(uint8_t CS, uint16_t* outputPointer)
{
  readRegister(CS, MLX90393_CONF1, outputPointer);
  readRegister(CS, MLX90393_CONF3, outputPointer+1);
}

/***********************************************************************************************/
