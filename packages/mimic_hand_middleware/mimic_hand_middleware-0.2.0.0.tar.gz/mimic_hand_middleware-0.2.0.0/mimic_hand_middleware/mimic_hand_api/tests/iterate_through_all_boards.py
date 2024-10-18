'''
Test code for basic functions of mimic_hand_api:
will iterate through all motors of a p4 hand and
apply different position cmds
'''
from time import sleep
import numpy as np
from mimic_hand_middleware.mimic_hand_api import RP2040Client as RP2040Client

def set_board_and_motor_idx_to_angle(
        boards_index: int,
        motor_index: int,
        angle: float = 0.0,
        ) -> None:
    '''
    Sets a motor to an angle, sets all other motors 0.0!
    '''
    cmd_dict = {
                2: {0: 0, 1: 0, 2: 0, 3: 0},
                3: {0: 0, 1: 0, 2: 0, 3: 0},
                4: {0: 0, 1: 0, 2: 0, 3: 0},
                5: {0: 0, 1: 0, 2: 0, 3: 0},
            }
    cmd_dict[boards_index][motor_index] = angle
    print("Commanding: ", cmd_dict)
    return cmd_dict


def main():
    client = RP2040Client()
    client.connect_all_motors()
    client.set_all_motors_to_cur_lim_pos_control_mode()
    for uart_id in client._motor_config["motor_board_uart_ids"]:
        for motor_id in range(4):
            print(f'Moving motor_id {motor_id} on uart_id {uart_id}')
            for _ in range(15):
                motor_pos_dict = set_board_and_motor_idx_to_angle(
                    uart_id, motor_id, 60.0)
                client.set_motor_positions(motor_pos_dict)
                sleep(1)
                motor_pos_dict = set_board_and_motor_idx_to_angle(
                    uart_id, motor_id, 0.0)
                client.set_motor_positions(motor_pos_dict)
                sleep(1)
            sleep(10)
    # Test middleware indexing as well (should be the same as the one in the
    # README.md)
    cmd_array_straight = np.zeros(16,)
    for _ in range(3):
        for i in range(1, 16):
            print("Moving motor of index: ", i)
            cmd_array_flexed = np.zeros(16,)
            client.command_middleware_motor_position_array(cmd_array_straight)
            sleep(0.01)
            for deg in range(20):
                cmd_array_flexed[i] = - float(deg)
                client.command_middleware_motor_position_array(
                    cmd_array_flexed)
                sleep(0.03)
            sleep(3)

    # Disconnect motors
    client.disconnect_all_motor_boards()


if __name__ == '__main__':
    main()
