"""
Calibrates the gripper and saves the new motor offsets in motor_config.yaml.
"""
# custom
import mimic_hand_middleware

if __name__ == '__main__':
    gripper_controller = mimic_hand_middleware.GripperController(
        calibrate_at_start=True,
        calibration_mode=True,
    )
    gripper_controller.disconnect_motors()
    print('Calibration ready! Shutting down.')
