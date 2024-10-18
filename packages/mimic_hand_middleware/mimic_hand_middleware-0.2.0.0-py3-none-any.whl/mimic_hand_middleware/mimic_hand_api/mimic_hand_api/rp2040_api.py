import time
from threading import RLock
from serial.serialutil import SerialException
import os

import numpy as np
import yaml

from .RP2040 import rp2040_client as rp2040


class RP2040Client:
    def __init__(self, port_name="/dev/ttyUSB0"):
        self.pico = rp2040.RP2040Client(portName=port_name)
        self.library_path = os.path.dirname(__file__)
        self._load_motor_map()
        self.client_lock = RLock()

    def _load_motor_map(self, yaml_file_name="motor_map.yaml") -> dict:
        '''
        Loads the motor map from the package folder, allowing for easier
        interfacing between the motors and the higher level APIs.
        Yaml path is given relative to the installation.
        '''
        yaml_path = os.path.join(
            self.library_path,
            yaml_file_name
        )
        with open(yaml_path, 'r') as motor_config_file:
            self._motor_config = yaml.safe_load(
                motor_config_file
            )
        self._motor_map = self._motor_config["motor_map"]
        self._inv_motor_map = self._get_inverted_motor_map()
        self._n_motors = len(self._motor_map.keys())
        self._uart_ids = list(self._motor_config["motor_board_uart_ids"])
        self._build_ros_idx_mapping(
            ros_motor_map=self._motor_config["middleware_convention_map"])
        print(f"Loaded motor map from {yaml_path}")

    def _get_inverted_motor_map(self) -> dict:
        '''
        Inverts the motor map so it can be used to look up conversions in the
        opposite directions as well
        '''
        inverse_motor_map = {}
        for k, v in self._motor_map.items():
            key_str = f'uart_{v["uart_id"]}_motor_{v["motor_id"]}'
            inverse_motor_map[key_str] = k
        return inverse_motor_map

    def _map_cmd_array_to_motors(
            self, cmd_angle_float_array: np.ndarray) -> dict:
        '''
        Takes a numpy array of shape (n_motors,) containing desired angle
        positions for the motors (in the convention detailed in the README)
        and converts it to a dict format that has the uart_id and the motor_id
        for each angle command.
        '''
        # takes around 40 us
        cmd_angle_dict = {}
        cmd_angle_float_array = cmd_angle_float_array.flatten()
        n_motors = len(self._motor_map.keys())
        assert len(cmd_angle_float_array) == n_motors, \
            f"Commanded angle shape {cmd_angle_float_array.shape} conflicts" +\
            f" with motor number {n_motors}"
        cmd_angle_float_list = [float(cmd_angle_float_array[i])
                                for i in range(cmd_angle_float_array.shape[0])]
        for motor_idx, cmd_angle_deg in enumerate(cmd_angle_float_list):
            uart_id = self._motor_map[motor_idx + 1]["uart_id"]
            motor_id = self._motor_map[motor_idx + 1]["motor_id"]
            if uart_id in cmd_angle_dict.keys():
                cmd_angle_dict[uart_id][motor_id] = cmd_angle_deg
            else:
                cmd_angle_dict[uart_id] = {motor_id: cmd_angle_deg}
        return cmd_angle_dict

    def _build_ros_idx_mapping(self, ros_motor_map: dict) -> None:
        '''
        Builds the numpy array of shape (n_motors,) that is used to remap the
        incoming motor commands (in the ROS middleware convention) to the
        low-level motor indexing used during wiring the tendons.
        '''
        n_motors_ROS = len(ros_motor_map.keys())
        assert n_motors_ROS == self._n_motors, f"N mot(l={self._n_motors})" +\
            f"not the same length as the ROS motor map (l={n_motors_ROS})"
        self._motor_idxes_ros_to_low_level = np.zeros((self._n_motors,))
        self._motor_idxes_low_level_to_ros = np.zeros((self._n_motors,))
        for middleware_motor_idx, low_level_motor_idx in ros_motor_map.items():
            self._motor_idxes_ros_to_low_level[low_level_motor_idx - 1] = \
                middleware_motor_idx
            self._motor_idxes_low_level_to_ros[middleware_motor_idx] = \
                low_level_motor_idx - 1
        self._motor_idxes_ros_to_low_level = \
            self._motor_idxes_ros_to_low_level.astype(np.uint16)
        self._motor_idxes_low_level_to_ros = \
            self._motor_idxes_ros_to_low_level.astype(np.uint16)
        print(f"Build ros idx mapping: {self._motor_idxes_ros_to_low_level}")
        print(f"Build low idx mapping: {self._motor_idxes_low_level_to_ros}")

    def command_motor_position_array(
            self, middleware_cmd_array: np.ndarray) -> None:
        '''
        Commands motor postions with a numpy array of shape (n_motors,).
        The motor commands are assumed to be in the low level wiring convention
        (see README.md).
        '''
        self.set_motor_positions(
            self._map_cmd_array_to_motors(middleware_cmd_array)
        )

    def command_middleware_motor_position_array(
            self, middleware_cmd_array: np.ndarray) -> None:
        '''
        Commands motor postions with a numpy array of shape (n_motors,).
        The motor commands are assumed to be in the ROS middleware convention
        (see README.md), and are converted to the low level motor indexing
        convention before the command is sent to the RP2040.
        '''
        low_level_cmd_array = middleware_cmd_array[
            self._motor_idxes_ros_to_low_level
        ]
        self.command_motor_position_array(low_level_cmd_array)

    def connect_motors(self, uart_id):
        status = False
        while not status:
            with self.client_lock:
                status = self.pico.initMotors(uart_id, [0, 1, 2, 3])
            if status:
                print(f"\033[92mConnected to UART ID {uart_id}!\033[0m")
            else:
                print(f"\033[91mError connecting to UART ID {uart_id}!\033[0m")
                val = input("Try again [y/n]? ")
                if val == "n":
                    print(
                        "\033[93mWarning:\033[0m Motors not connected for",
                        f" muscle group UART ID {uart_id}"
                    )
                    break
        print("\n\n".rjust(102, "-"))
        return status

    def connect_all_motors(self) -> None:
        '''
        Connects all motor boards with uart ids specified in motor_map.yaml/
        motor_board_uart_ids.
        '''
        for uart_id in self._uart_ids:
            if not self.connect_motors(uart_id):
                print(f"Problem connecting UART ID {uart_id}!")

    def set_motor_mode(self, uart_id, mode):
        with self.client_lock:
            self.pico.stopProcess()
        status = False
        while not status:
            with self.client_lock:
                status = self.pico.setMotorMode(uart_id, mode)
            if status:
                print(
                    f"\033[92mSuccess setting motor mode {mode} for ",
                    f"UART ID {uart_id}!\033[0m"
                )
            else:
                print(
                    f"\033[91mError setting motor mode {mode} for ",
                    f"UART ID {uart_id}!\033[0m"
                )
                val = input("Try again [y/n]? ")
                if val == "n":
                    break
        if status:
            with self.client_lock:
                self.pico.process(mode)
        else:
            print(
                "\033[93mWarning:\033[0m Did not set motor mode",
                f" for UART ID {uart_id}"
            )
        print("\n\n".rjust(102, "-"))
        return status

    def _set_motor_cur_limit(self, uart_id, cur_limit_mA):
        '''
        Sets the current limit (in Amperes) on the motors attached to the board
        with uart_id
        '''
        cur_limit_mA = int(cur_limit_mA)
        with self.client_lock:
            self.pico.stopProcess()
        status = False
        while not status:
            with self.client_lock:
                status = self.pico.setCurrentLimit(uart_id, cur_limit_mA)
            if status:
                print(
                    f"\033[92mSuccess setting motor cur {cur_limit_mA} for",
                    f" UART ID {uart_id}!\033[0m"
                )
            else:
                print(
                    f"\033[91mError setting motor cur {cur_limit_mA} for ",
                    f"UART ID {uart_id}!\033[0m"
                )
                val = input("Try again [y/n]? ")
                if val == "n":
                    break
        if not status:
            print(
                "\033[93mWarning:\033[0m Did not set motor mode",
                f" for UART ID {uart_id}"
            )
        print("\n\n".rjust(102, "-"))
        return status

    def set_all_motors_to_cur_lim_pos_control_mode(self) -> None:
        '''
        Sets all motors to current limited position control mode. The motors
        are set through the driver boards, the uart_ids of the driver boards
        attached are specified in motor_map.yaml/motor_board_uart_ids.
        '''
        for uart_id in self._uart_ids:
            if not self.set_motor_mode(
                 uart_id, rp2040.MOTOR_CUR_LIM_POS_CTRL):
                print(f"Problem setting motor mode for UART ID {uart_id}!")

    def set_all_motors_to_freerunning_mode(self) -> None:
        '''
        Sets all motors to a free running mode mode. The motors are set through
        the driver boards, the uart_ids of the driver boards attached are
        specified in motor_map.yaml/motor_board_uart_ids.
        '''
        for uart_id in self._uart_ids:
            if not self.set_motor_mode(
                 uart_id, rp2040.MOTOR_CALIBRATE):
                print(f"Problem setting motor mode for UART ID {uart_id}!")

    def set_current_limit(self, current_limit_mA: float) -> None:
        '''
        Sets the current limit on the motors
        '''
        for uart_id in self._uart_ids:
            if not self._set_motor_cur_limit(uart_id, current_limit_mA):
                print(f"Problem setting motor current for UART ID {uart_id}!")

    def get_motor_currents_raw(self):
        '''
        Returns the motor currents in the motor command-level indexing
        convention. (with uart_id, motor_id pairs, as a dict)
        '''
        motor_currents = self.pico.getMotorCurrents()
        return motor_currents

    def get_motor_currents(self):
        '''
        Returns the motor currents in the middleware-level indexing
        convention, as a numpy array of shape (n_motors,) in milliAmpéres.
        '''
        raw_motor_currents = self.get_motor_currents_raw()
        motor_current_array = self._remap_motor_measurement_to_middleware(
            input_dict=raw_motor_currents
        )
        return motor_current_array

    def get_motor_positions_raw(self):
        '''
        Returns the motor positions in the motor command-level indexing
        convention, as angles (with uart_id, motor_id pairs, as a dict)
        '''
        motor_positions = self.pico.getMotorPositions()
        return motor_positions

    def get_motor_positions(self):
        '''
        Returns the motor positions in the middleware-level indexing
        convention, as a numpy array of shape (n_motors,), in angles
        '''
        raw_motor_positions = self.get_motor_positions_raw()
        motor_positions_array = self._remap_motor_measurement_to_middleware(
            input_dict=raw_motor_positions
        )
        return motor_positions_array

    def _remap_motor_measurement_to_middleware(
            self,
            input_dict: dict) -> np.ndarray:
        '''
        Formats an incoming measurement in the low level motor command format
        to a middleware-level array format
        '''
        output_array = np.zeros((self._n_motors))
        for uart_id, motor_pos_dict in input_dict.items():
            for motor_id, measured_value in motor_pos_dict.items():
                idx = self._inv_motor_map[
                        f"uart_{uart_id}_motor_{motor_id}"]
                output_array[self._motor_idxes_low_level_to_ros[idx-1]] = \
                    measured_value
        return output_array

    def set_motor_positions(self, motor_pos_dict: dict):
        '''
        Sets motor positions for each UART id. Positions are given in the
        motor_pos_dict in the following form:
        {uart_id_1: {motor_id_1: angle_1,...}, uard_id_2 : {motor_id_2: ...}}
        '''
        cmd = {}
        for uart_id, position_dict in motor_pos_dict.items():
            cmd[uart_id] = position_dict
        self.pico.setMotorPositions(cmd)

    def disconnect_motors(self, uart_id: int, retry_sleep_len_s: float = 1.0):
        print(f"Disconnecting motors for UART ID {uart_id}...")
        disconnected = False
        while not disconnected:
            try:
                self.pico.setMotorMode(uart_id, rp2040.MOTOR_OFF)
                disconnected = True
            except SerialException:
                print(f"Could not disconnect UART ID {uart_id}")
                print(f"Sleeping {retry_sleep_len_s} s and trying again..")
                time.sleep(retry_sleep_len_s)

        print(f"Motors disconnected for UART ID {uart_id}.")
        time.sleep(4)

    def disconnect_all_motor_boards(self) -> None:
        '''
        Disconnects all motor boards specified by motor_map.yaml/
        motor_board_uart_ids.
        '''
        # disconnect motors
        for uart_id in self._uart_ids:
            self.disconnect_motors(uart_id)
        # stop reading and terminate serial
        self.pico.stopProcess()
        self.pico.closePort()


def test():
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

    for _ in range(3):
        client.set_motor_positions(
            {
                2: {0: 0, 1: 0, 2: 0, 3: 0},
                3: {0: 0, 1: 0, 2: 0, 3: 0},
            })
        time.sleep(2)
        client.set_motor_positions(
            {
                2: {0: -90, 1: 0, 2: 0, 3: 0},
                3: {0: -90, 1: 0, 2: 0, 3: 0},
            })
        time.sleep(2)

    cmd_array_straight = np.zeros(16,)
    cmd_array_flexed = np.zeros(16,)
    cmd_array_flexed[6:9] = - 90
    for _ in range(3):
        client.set_motor_positions(
            client._map_cmd_array_to_motors(cmd_array_straight)
        )
        time.sleep(3)
        client.set_motor_positions(
            client._map_cmd_array_to_motors(cmd_array_flexed)
        )
        time.sleep(3)

    # Get motor currents
    client.get_motor_currents()

    # Get motor positions
    client.get_motor_positions()

    # Disconnect motors
    for uart_id in uart_ids:
        client.disconnect_motors(uart_id)


if __name__ == "__main__":
    test()
