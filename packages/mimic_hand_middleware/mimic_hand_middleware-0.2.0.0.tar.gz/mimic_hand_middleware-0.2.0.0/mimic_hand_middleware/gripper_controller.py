"""
High level file providing access to the middleware of the hand prototypes from
P04 onwards.

Made by Benedek Forrai (ben.forrai@mimicrobotics.com)
"""

# standard
import os
import pathlib
import sys
import time
from copy import deepcopy
from threading import RLock

# third-party
import numpy as np
import yaml

# custom
from .conversion_utils import p04 as hand_utils
from .kinematics.hand_kinematics import HandKinematics

from mimic_hand_middleware.mimic_hand_api import RP2040Client as DriverClient


class GripperController:
    """
    Middleware level class for controlling mimic's robotic hands for prototypes
    newer than P04.
    Provides the following methods for easier integration:
    - connect_to_motors: connects to the motors of the hand to the API
    - init_joints: "homes" the hands and starts the EKF tracking if specified.
    - command_joint_angles: sends the desired joint (!) angles to the hand. The
        hand then takes a motor configuration that is as close to the commanded
        joint angles as possible.
    - get_joint_pos: returns the current position of the joints (in deg.)
    - get_joint_vel: returns the speed of the joints (in deg./s)
    - get_motor_pos_vel_cur: returns the position (deg), rot. speed (deg/s) and
        current (mA) of the motors
    """

    def __init__(
        self,
        prototype_name: str = 'p4',
        port: str = '/dev/mimic_hand_driver',
        config_yml: str = 'p_0_4.yaml',
        motor_config_yml: str = 'motor_config.yaml',
        init_motor_pos_update_thread: bool = True,
        use_sim_joint_measurement: bool = False,
        compliant_test_mode: bool = False,
        max_motor_current: float = 200.0,
        use_sim_motors: bool = False,
        calibrate_at_start: bool = False,
        calibration_mode: bool = False,
        motor_port_env_var: str = 'HAND_PORT',
    ) -> None:
        """
        The controller has the following parameters:
        - prototype_name (str): name of the hand prototype that is currently in
            use
        - port (str): name of the USB port to connect to
        - config_yml (str): name of config file defining the MuscleGroups in a
            hand. Legacy, kept only for backwards compatibility
        - init_motor_pos_update_thread (bool): legacy, kept only for
            compatibility
        - use_sim_joint_measurement (bool): whether to run the EKF tracker
        - compliant_test_mode (bool): legacy, kept only for compatibility
        (not back-driveable currently sadly)
        - max_motor_current (float): maximum allowed motor current in mA
        - use_sim_motors (bool): if set to true, run a virtual simple sim of
            the hand
        """
        # Init class variables
        self._prototype = prototype_name
        self._cfg_file_name = config_yml
        self._motor_cfg_file_name = motor_config_yml
        self._init_pos_update = init_motor_pos_update_thread
        self._sim_measurement = use_sim_joint_measurement
        self._sim_motors = use_sim_motors
        self._compliant_mode_legacy = compliant_test_mode
        self._max_motor_current = max_motor_current
        # Init port for hand communication
        if motor_port_env_var in os.environ.keys():
            self._port = '/dev/' + str(os.environ[motor_port_env_var])
        else:
            self._port = port
        # Import/init low-level utilities
        self._hand_kinematics = HandKinematics(yaml_name=self._cfg_file_name)
        hand_utils.init_matrices()
        # Init constants
        self.num_of_joints = len(hand_utils.JOINT_NAMES_NORMAL)
        self.joint_names = hand_utils.JOINT_NAMES_NORMAL
        self.joint_limit_lower = hand_utils.GC_LIMITS_LOWER
        self.joint_limit_higher = hand_utils.GC_LIMITS_UPPER
        self.num_of_motors = len(hand_utils.MOTOR_NAMES)
        self._motor_zero_offsets = np.zeros((self.num_of_motors,))
        self.motors_limit_lower = hand_utils.MOTOR_LIMIT_LOWER
        self.motors_limit_higher = hand_utils.MOTOR_LIMIT_HIGHER
        self.motors_mcp_to_mean_delta = hand_utils.MCP_TO_MEAN_DELTA
        self.motors_mcp_from_mean_delta = hand_utils.MCP_FROM_MEAN_DELTA
        self.torque_enabled = False
        # Disable scientific notation for printing np arrays
        np.set_printoptions(suppress=True)
        if calibrate_at_start:
            self.connect_motors()
            self._calibrate_motor_angles()
        else:
            try:
                self._motor_config = yaml.safe_load(
                    pathlib.Path(
                        os.path.join(
                            os.path.dirname(os.path.realpath(__file__)),
                            self._motor_cfg_file_name,
                        )
                    ).read_text()
                )
                self._motor_zero_offsets = np.array(
                    self._motor_config['zero_offsets']
                ).reshape((-1,))
                print('motor offset: ', self._motor_zero_offsets)
            except FileNotFoundError:
                print('Failed to find motor_config.yaml!')

    def connect_motors(self) -> None:
        """
        Connects to the motors of the hand.
        If self._sim_motors is True, does not do
        anything.
        """
        if not self._sim_motors and not hasattr(self, '_driver_client'):
            self._driver_client = DriverClient(port_name=self._port)
            self._driver_client.connect_all_motors()
            self._driver_client.set_current_limit(self._max_motor_current)
            self._driver_client.set_all_motors_to_cur_lim_pos_control_mode()
        else:
            pass

    def disconnect_motors(self) -> None:
        """
        Disconnects motors from all boards.
        If self.sim_motors is True, does not do anything.
        """
        if not self._sim_motors:
            self._driver_client.disconnect_all_motor_boards()
            print('Disconnected all motors. Controller can be shut down now!')
        else:
            pass

    def enable_torque(self) -> None:
        """
        Sets the motors to current-limited positional control mode.
        """
        self._driver_client.set_all_motors_to_cur_lim_pos_control_mode()
        self.torque_enabled = True

    def disable_torque(self) -> None:
        """
        Sets the motors to freerunning mode.
        """
        self._driver_client.set_all_motors_to_freerunning_mode()
        self.torque_enabled = False

    def init_joints(self, calibrate: bool = False) -> None:
        """
        Initializes the internal buffers of the hand and "homes" it to its zero
        position.
        If calibrate is set to True, calibrates the hand by driving it to its
        limit positions and registering motor positions.
        """
        self._motor_lock = RLock()
        self._joint_value_lock = RLock()
        # set zero initial position
        with self._joint_value_lock:
            self._joint_array = np.zeros((self.num_of_joints,))
        if not self._sim_motors:
            if calibrate:
                self._calibrate_motor_angles()
                # enable torque again
                self.enable_torque()

    def _get_motor_angles_from_tendon_lengths(
        self, commanded_lengths: np.ndarray
    ) -> None:
        """
        Get motor angles (uncalibrated) from free tendon lenghts.
        @param commanded_lengths (np.ndarray of shape (num_of_motors,)):
            the commanded lengths (in meters) for each of the 16 tendons.
        @return motor_angles (np.ndarray of shape (num_of_motors,)): motor
            angles that result in the desired tendon lengths, in radians.
        """
        return commanded_lengths / self._hand_kinematics.spool_rad

    def command_joint_angles(
        self, commanded_angles: np.ndarray, convert_from_degrees: bool = True
    ) -> None:
        """
        Commands joint angle command_angles (in degrees) to the low level
        controller. If self._sim_motors is True, this only updates the current
        commanded joint array.
        """
        commanded_angles = deepcopy(commanded_angles)
        commanded_angles = self._filter_joint_angle_limits(commanded_angles)
        if convert_from_degrees:
            commanded_angles *= np.pi / 180
        commanded_angles = commanded_angles.reshape((-1,))
        assert commanded_angles.shape[0] == self.num_of_joints, (
            'Incorrect command dimension; got commanded shape of'
            + f' {commanded_angles.shape} while number of joints is '
            + f'{self.num_of_joints}!'
        )
        if not self._sim_motors:
            free_tendon_lengths = self._get_tendon_lengths_from_angles(commanded_angles)
            raw_spool_angles = self._get_motor_angles_from_tendon_lengths(
                free_tendon_lengths
            )
            self.command_motor_angles(
                commanded_angles=raw_spool_angles, convert_from_radians=True
            )
        else:
            with self._joint_value_lock:
                self._joint_array = commanded_angles

    def _get_tendon_lengths_from_angles(self, angles_rad: np.ndarray) -> np.ndarray:
        """
        Calculates the desired "free" (difference from normal pos.) tendon
        length (in meters) from the desire joint array.
        """
        tendon_lengths = (
            self._hand_kinematics.get_tendon_lengths_m_from_joint_angles_rad(angles_rad)
        )
        return tendon_lengths

    def _get_calibrated_motor_angles(self, raw_spool_angles: np.ndarray) -> np.ndarray:
        """
        Takes uncalibrated motor angle commands (in radians) and shifts them
        with the zero positions measured during calibration.
        """
        motor_angles = raw_spool_angles + self._motor_zero_offsets
        return motor_angles

    def _filter_joint_angle_limits(self, raw_joint_angles: np.ndarray) -> np.ndarray:
        """
        Filters raw_joint_angles (assumed to be in degrees) to stay inside the
        joint limits.
        """
        filtered_joint_angles = np.clip(
            a=raw_joint_angles,
            a_min=self.joint_limit_lower,
            a_max=self.joint_limit_higher,
        )
        return filtered_joint_angles

    def command_motor_angles(
        self, commanded_angles: np.ndarray, convert_from_radians: bool = False
    ) -> None:
        """
        Commands desired motor angles (in degrees)
        """
        cmd_angles = deepcopy(commanded_angles)
        if convert_from_radians:
            cmd_angles = np.rad2deg(cmd_angles)
        cmd_angles = self._get_calibrated_motor_angles(cmd_angles)
        self._driver_client.command_middleware_motor_position_array(cmd_angles)

    def get_joint_pos(self, use_ekf: bool = True) -> np.ndarray:
        """
        Returns the joint position array of the hand in degrees
        """
        joint_array = np.zeros((self.num_of_joints))
        with self._joint_value_lock:
            joint_array = deepcopy(self._joint_array)
        return joint_array

    def get_joint_vel(self) -> np.ndarray:
        """
        Returns the joint velocity array of the hand in degrees/s
        """
        if not self._sim_motors:
            # TODO later this needs to come from the jacobian
            joint_vel_array = np.zeros((self.num_of_joints, 1))
        else:
            joint_vel_array = np.zeros((self.num_of_joints, 1))
        return joint_vel_array

    def get_motor_pos_vel_cur(self) -> np.ndarray:
        """
        Returns the position (degrees), velocity (degrees/s) and current (mA)
        measured by the motors
        """
        motor_pos = np.zeros((self.num_of_motors,))
        motor_vel = np.zeros((self.num_of_motors,))
        motor_cur = np.zeros((self.num_of_motors,))
        if not self._sim_motors:
            motor_cur = self._driver_client.get_motor_currents()
            motor_pos = self._driver_client.get_motor_positions()
        return motor_pos, motor_vel, motor_cur

    def _calibrate_motor_group(
        self,
        motor_group_idxes: np.ndarray,
        forward_max_current_mA: float,
        backward_max_current_mA: float,
        starting_resolution_deg: float = 5.0,
        resolution_refine_steps: int = 2,
        resolution_refine_scale: float = 5.0,
    ) -> list:
        """
        Moves the motors selected by motor_group_idxes (with the middleware
        convention, see README.md) to the joint limits in both directions,
        until the respective current limit (forward/backward_max_current_mA) is
        hit. Repeats the test of the limit with smaller steps than the starting
        step size (starting_resolution_deg), with each step cycle scaled by
        1/resolution_refine_scale.
        """
        print(f'Calibrating motor group idxes: {motor_group_idxes}')
        step_sizes = [
            starting_resolution_deg / (resolution_refine_scale**i)
            for i in range(resolution_refine_steps)
        ]
        # calibrate positive direction
        start_angles = np.zeros_like(motor_group_idxes)
        for step_size in step_sizes:
            self._drive_group_until_limit(
                motor_group_idxes,
                max_current_mA=forward_max_current_mA,
                step=step_size,
                start_angles=start_angles,
            )
            limit_pos = self._driver_client.get_motor_positions()
            start_angles = limit_pos[motor_group_idxes] * 0.75
            time.sleep(0.5)
        forward_limit_pos = limit_pos[motor_group_idxes]
        # calibrate negative direction
        start_angles = np.zeros_like(motor_group_idxes)
        self._driver_client.command_middleware_motor_position_array(
            middleware_cmd_array=np.zeros((self.num_of_motors,))
        )
        # delay for currents to got back to normal
        time.sleep(0.5)
        for step_size in step_sizes:
            self._drive_group_until_limit(
                motor_group_idxes,
                max_current_mA=backward_max_current_mA,
                step=-step_size,
                start_angles=start_angles,
            )
            limit_pos = self._driver_client.get_motor_positions()
            start_angles = deepcopy(limit_pos[motor_group_idxes])
            start_angles *= 0.75
            time.sleep(0.5)
        backward_limit_pos = limit_pos[motor_group_idxes]
        return [forward_limit_pos, backward_limit_pos]

    def _drive_group_until_limit(
        self,
        motor_group_idxes: np.ndarray,
        max_current_mA: float,
        step: float,
        start_angles: np.ndarray = None,
    ) -> None:
        """
        Moves the motors selected by motor_group_idxes (with the middleware
        convention, see README.md) with step until max_current_mA is hit. Sends
        the rest of the motors to 0 deg.
        """
        # init start angle
        motor_group_idxes = motor_group_idxes.reshape(-1)
        cmd_array = np.zeros((self.num_of_motors,))
        if start_angles is not None:
            cmd_array[motor_group_idxes] = start_angles
        # drive motor group to limit from start angle
        driven_group_cmd_array = cmd_array[motor_group_idxes]
        motor_cur = self._driver_client.get_motor_currents()
        while np.any(motor_cur[motor_group_idxes] < max_current_mA):
            driven_group_cmd_array[motor_cur[motor_group_idxes] < max_current_mA] += (
                step
            )
            cmd_array[motor_group_idxes] = driven_group_cmd_array
            self._driver_client.command_middleware_motor_position_array(cmd_array)
            time.sleep(abs(0.02 * step))
            motor_cur = self._driver_client.get_motor_currents()
            print('motor cur: ', motor_cur)

    def _calibrate_motor_angles(self) -> None:
        """
        Reads the zero positions of the motors and writes them to a yaml file.
        """
        self.get_new_motor_zero_positions()
        motor_dict = self._get_motor_dict()
        cfg_file_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            self._motor_cfg_file_name,
        )
        with open(cfg_file_name, 'w') as cfg_file:
            yaml.safe_dump(
                data=motor_dict,
                stream=cfg_file,
            )
            print('Saved calibration results and applied calibration!')

    def _get_motor_dict(self) -> dict:
        """
        Assembles a motor dict from the current state of the motors that
        we can write to a calibration file.
        """
        motor_zero_offsets = self._motor_zero_offsets
        motor_dict = {
            'zero_offsets': [float(offset) for offset in list(motor_zero_offsets)]
        }
        return motor_dict

    def get_new_motor_zero_positions(self) -> None:
        """
        Recalibrates the offsets for the motors such that the current position
        will be treated as the new zero position during operation.
        """
        # turn motors to freerunning mode
        self.disable_torque()
        input('Move to new zero position then press Enter!')
        self._motor_zero_offsets = self._driver_client.get_motor_positions()
