#ifndef __FAIVE_UART_H__
#define __FAIVE_UART_H__

#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/irq.h"

#define UART_ID         uart0
#define BAUDRATE        115200
#define DATA_BITS       8
#define STOP_BITS       1
#define PARITY          UART_PARITY_NONE

#define UART_TX_PIN     0
#define UART_RX_PIN     1

#define DE_PIN          2

#define DEVICE_ID       '3'

void initUART(void);
void UART_read(void);
bool UART_write(char device, char function, char* data, uint8_t len);
void processMessage(char* msg, uint8_t len);
uint16_t calculateCRC16(const char* message, uint8_t len);
uint16_t reflect(uint16_t data, uint8_t len);

#endif // End of __FAIVE_UART_H__ definition check