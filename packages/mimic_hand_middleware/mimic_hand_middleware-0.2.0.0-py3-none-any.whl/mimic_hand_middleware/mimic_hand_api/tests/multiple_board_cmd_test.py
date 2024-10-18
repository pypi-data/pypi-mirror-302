'''
Test code for basic functions of mimic_hand_api:
will iterate through all motors of a p4 hand and
apply different position cmds
'''
from time import sleep
from mimic_hand_middleware.mimic_hand_api import RP2040Client as RP2040Client
import mimic_hand_middleware.mimic_hand_api.mimic_hand_api.RP2040.rp2040_client as rp2040


def main():
    client = RP2040Client()
    # Initialize and connect motors for UART ID 1 and 2
    uart_ids = [2, 3, 4, 5]

    for uart_id in uart_ids:
        if not client.connect_motors(uart_id):
            print(f"Problem connecting UART ID {uart_id}!")

    # Set motor mode to current-limited position control for both UART IDs
    for uart_id in uart_ids:
        if not client.set_motor_mode(uart_id, rp2040.MOTOR_CUR_LIM_POS_CTRL):
            print(f"Problem setting motor mode for UART ID {uart_id}!")

    for _ in range(2):
        client.set_motor_positions(
            {
                2: {0: 0, 1: 0, 2: 0, 3: 0},
                3: {0: 0, 1: 0, 2: 0, 3: 0},
            })
        sleep(2)
        client.set_motor_positions(
            {
                2: {0: -90, 1: 0, 2: 0, 3: 0},
                3: {0: -90, 1: 0, 2: 0, 3: 0},
            })
        sleep(2)

    # Get motor currents
    currents = client.get_motor_currents()

    # Get motor positions
    positions = client.get_motor_positions()

    print(f"Got currents: {currents} and positions {positions}")

    # Set motor mode to free running for UART ID 1
    # client.set_motor_mode(2, rp2040.MOTOR_CALIBRATE)
    # print("done")

    # Disconnect motors
    for uart_id in uart_ids:
        client.disconnect_motors(uart_id)


if __name__ == '__main__':
    main()
