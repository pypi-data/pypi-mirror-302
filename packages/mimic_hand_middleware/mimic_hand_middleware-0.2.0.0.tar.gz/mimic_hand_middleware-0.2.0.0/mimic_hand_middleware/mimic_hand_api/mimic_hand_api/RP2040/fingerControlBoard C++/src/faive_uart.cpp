#include "main.h"
#include "faive_uart.h"
#include "stdio.h"

const uint16_t crcTable[256] =
{
    0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
    0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
    0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
    0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
    0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
    0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
    0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
    0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
    0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
    0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
    0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
    0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
    0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
    0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
    0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
    0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
    0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
    0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
    0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
    0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
    0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
    0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
    0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
    0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
    0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
    0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
    0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
    0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
    0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
    0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
    0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
    0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
};

void initUART(void)
{
    // initialize DE pin
    gpio_init(DE_PIN);
    gpio_set_dir(DE_PIN, GPIO_OUT);
    gpio_put(DE_PIN, 0);

    // Initialize UART
    uart_init(UART_ID, BAUDRATE);

    // Set function of gpio pins to UART
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);

    // Turn off UART flow control CTS/RTS
    uart_set_hw_flow(UART_ID, false, false);

    // Set UART format
    uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);

    // Turn off FIFO
    uart_set_fifo_enabled(UART_ID, false);

    // Set up and enable the interrupt handlers
    irq_set_exclusive_handler(UART0_IRQ, UART_read);
    irq_set_enabled(UART0_IRQ, true);

    uart_set_irq_enables(UART_ID, true, false);
}

// RX interrupt handler
void UART_read(void)
{
    static bool reading = false;
    static char rx_char = 0;
    static char prev_rx_char = 0;
    static char rxData[50];
    static uint8_t index;

    while (uart_is_readable(UART_ID))
    {
        prev_rx_char = rx_char;
        rx_char = uart_getc(UART_ID);

        if (rx_char == ':')
        {
            reading = true;
            index = 0;
            continue;
        }

        if (reading)
        {
            if(rx_char == 10 && prev_rx_char == 13)
            {
                reading = false;
                processMessage(rxData, index-1);
            }

            rxData[index++] = rx_char;
        }
    }
}

bool UART_write(char device, char function, char* data, uint8_t len)
{
    uint8_t msg_len = len + 7;
    char message[msg_len];
    uint16_t CRC;

    // Start of message
    message[0] = ':';

    // Device ID and instruction
    message[1] = device;
    message[2] = function;

    // Data
    for (int i = 0; i < len; i++)
    {
        message[i+3] = *(data+i);
    }

    // CRC
    CRC = calculateCRC16(data, len);
    message[msg_len - 4] = (uint8_t) ((CRC & 0xFF00) >> 8);
    message[msg_len - 3] = (uint8_t) (CRC & 0x00FF);

    // End of Line
    message[msg_len - 2] = 13;
    message[msg_len - 1] = 10;

    if (uart_is_writable(UART_ID))
    {
        gpio_put(DE_PIN, 1);
        uart_write_blocking(UART_ID, (uint8_t*) message, msg_len);
        uart_tx_wait_blocking(UART_ID);
        gpio_put(DE_PIN, 0);
        return true;
    } else {
        return false;
    }
}

void processMessage(char* msg, uint8_t len)
{
    char device;
    char function;
    char data[50];
    uint16_t rx_CRC;
    uint16_t CRC;

    device = *msg;
    function = *(msg + 1);

    for (int i = 0; i < len - 4; i++)
    {
        data[i] = *(msg + 2 + i);
    }

    rx_CRC = ((uint16_t) *(msg + len - 1)) | (((uint16_t) *(msg + len - 2)) << 8);

    // Check CRC
    CRC = calculateCRC16(data, len - 4);
    if (CRC != rx_CRC)
    {
        error_handler();
    }

    // TODO: do something
    printf("Received data for device %c. Instruction %c with data: ", device, function);
    puts(data);
    printf("\n\n");
}

uint16_t calculateCRC16(const char* message, uint8_t len)
{
    uint8_t data;
    uint16_t remainder = 0;

    for (int i = 0; i < len; i++)
    {
        data = ((uint8_t) reflect(*(message+i), 8)) ^ (remainder >> 8);
        remainder = crcTable[data] ^ (remainder << 8);
    }

    return reflect(remainder, 16);
}

uint16_t reflect(uint16_t data, uint8_t len)
{
    uint16_t reflection;

    for (int i = 0; i < len; i++)
    {
        if (data & 0x01)
        {
            reflection |= 1 << (len - 1 - i);
        }

        data = data >> 1;
    }

    return reflection;
}
