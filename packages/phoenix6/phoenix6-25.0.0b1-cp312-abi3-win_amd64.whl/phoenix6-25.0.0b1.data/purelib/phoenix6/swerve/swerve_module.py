"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from enum import Enum
from typing import overload
from threading import RLock
from phoenix6.units import newton
from phoenix6.hardware.cancoder import CANcoder
from phoenix6.hardware.talon_fx import TalonFX
from phoenix6.hardware.parent_device import SupportsSendRequest
from phoenix6.signals.spn_enums import FeedbackSensorSourceValue, InvertedValue, NeutralModeValue
from phoenix6.swerve.utility.geometry import *
from phoenix6.swerve.utility.kinematics import *
from phoenix6.swerve.swerve_module_constants import SwerveModuleConstants, SteerFeedbackType
from phoenix6.phoenix_native import Native, SwerveModuleRequest_t, SwerveModuleState_t

class SwerveModule:
    """
    Swerve Module class that encapsulates a swerve module powered by CTR
    Electronics devices.

    This class handles the hardware devices and configures them for
    swerve module operation using the Phoenix 6 API.

    This class constructs hardware devices internally, so the user
    only specifies the constants (IDs, PID gains, gear ratios, etc).
    Getters for these hardware devices are available.

    :param constants:       Constants used to construct the module
    :type constants:        SwerveModuleConstants
    :param canbus_name:     The name of the CAN bus this module is on
    :type canbus_name:      str
    :param drivetrain_id:   ID of the swerve drivetrain
    :type drivetrain_id:    int
    :param index:           Index of this swerve module
    :type index:            int
    """

    class SteerRequestType(Enum):
        """
        All possible control requests for the module steer motor.
        """

        MOTION_MAGIC_EXPO = 0
        """
        Control the drive motor using a Motion Magic® Expo request.
        The control output type is determined by SwerveModuleConstants.SteerMotorClosedLoopOutput
        """
        POSITION = 1
        """
        Control the drive motor using an unprofiled position request.
        The control output type is determined by SwerveModuleConstants.SteerMotorClosedLoopOutput
        """

    class DriveRequestType(Enum):
        OPEN_LOOP_VOLTAGE = 0
        """
        Control the drive motor using an open-loop voltage request.
        """
        VELOCITY = 1
        """
        Control the drive motor using a velocity closed-loop request.
        The control output type is determined by SwerveModuleConstants.DriveMotorClosedLoopOutput
        """

    class ModuleRequest:
        """
        Contains everything the swerve module needs to apply a request.
        """

        def __init__(self):
            self.state = SwerveModuleState()
            """
            Unoptimized speed and direction the module should target.
            """

            self.wheel_force_feedforward_x: newton = 0.0
            """
            Robot-relative wheel force feedforward to apply in the
            X direction. X is defined as forward according to WPILib
            convention, so this determines the forward force to apply.

            This force should include friction applied to the ground.
            """
            self.wheel_force_feedforward_y: newton = 0.0
            """
            Robot-relative wheel force feedforward to apply in the
            Y direction. Y is defined as to the left according to WPILib
            convention, so this determines the force to apply to the left.

            This force should include friction applied to the ground.
            """

            self.drive_request = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
            """
            The type of control request to use for the drive motor.
            """
            self.steer_request = SwerveModule.SteerRequestType.MOTION_MAGIC_EXPO
            """
            The type of control request to use for the steer motor.
            """

        def with_state(self, new_state: SwerveModuleState) -> 'SwerveModule.ModuleRequest':
            """
            Modifies the state parameter and returns itself.

            Unoptimized speed and direction the module should target.

            :param new_state: Parameter to modify
            :type new_state: SwerveModuleState
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.state = new_state
            return self

        def with_wheel_force_feedforward_x(self, new_wheel_force_feedforward_x: newton) -> 'SwerveModule.ModuleRequest':
            """
            Modifies the wheel_force_feedforward_x parameter and returns itself.

            Robot-relative wheel force feedforward to apply in the
            X direction. X is defined as forward according to WPILib
            convention, so this determines the forward force to apply.

            This force should include friction applied to the ground.

            :param wheel_force_feedforward_x: Parameter to modify
            :type wheel_force_feedforward_x: newton
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.wheel_force_feedforward_x = new_wheel_force_feedforward_x
            return self

        def with_wheel_force_feedforward_y(self, new_wheel_force_feedforward_y: newton) -> 'SwerveModule.ModuleRequest':
            """
            Modifies the wheel_force_feedforward_y parameter and returns itself.

            Robot-relative wheel force feedforward to apply in the
            Y direction. Y is defined as to the left according to WPILib
            convention, so this determines the force to apply to the left.

            This force should include friction applied to the ground.

            :param wheel_force_feedforward_y: Parameter to modify
            :type wheel_force_feedforward_y: newton
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.wheel_force_feedforward_y = new_wheel_force_feedforward_y
            return self

        def with_drive_request(self, new_drive_request: 'SwerveModule.DriveRequestType') -> 'SwerveModule.ModuleRequest':
            """
            Modifies the drive_request parameter and returns itself.

            The type of control request to use for the drive motor.

            :param new_drive_request: Parameter to modify
            :type new_drive_request: SwerveModule.DriveRequestType
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.drive_request = new_drive_request
            return self

        def with_steer_request(self, new_steer_request: 'SwerveModule.SteerRequestType') -> 'SwerveModule.ModuleRequest':
            """
            Modifies the steer_request parameter and returns itself.

            The type of control request to use for the steer motor.

            :param new_steer_request: Parameter to modify
            :type new_steer_request: SwerveModule.SteerRequestType
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.steer_request = new_steer_request
            return self

    def __init__(self, constants: SwerveModuleConstants, canbus_name: str, drivetrain_id: int, index: int):
        self._drivetrain = drivetrain_id
        self._module_idx = index

        self._internal_state = SwerveModulePosition()
        self._current_state = SwerveModuleState()
        self._target_state = SwerveModuleState()
        self._state_lock = RLock()

        self._drive_motor = TalonFX(constants.drive_motor_id, canbus_name)
        self._steer_motor = TalonFX(constants.steer_motor_id, canbus_name)
        self._cancoder = CANcoder(constants.cancoder_id, canbus_name)

        drive_configs = constants.drive_motor_initial_configs
        drive_configs.motor_output.neutral_mode = NeutralModeValue.BRAKE

        drive_configs.slot0 = constants.drive_motor_gains
        drive_configs.torque_current.peak_forward_torque_current = constants.slip_current
        drive_configs.torque_current.peak_reverse_torque_current = -constants.slip_current
        drive_configs.current_limits.stator_current_limit = constants.slip_current
        drive_configs.current_limits.stator_current_limit_enable = True

        drive_configs.motor_output.inverted = (
            InvertedValue.CLOCKWISE_POSITIVE
            if constants.drive_motor_inverted
            else InvertedValue.COUNTER_CLOCKWISE_POSITIVE
        )
        response = self.drive_motor.configurator.apply(drive_configs)
        if not response.is_ok():
            print(f"TalonFX ID {self.drive_motor.device_id} failed config with error {response.name}")

        steer_configs = constants.steer_motor_initial_configs
        steer_configs.motor_output.neutral_mode = NeutralModeValue.BRAKE

        steer_configs.slot0 = constants.steer_motor_gains
        # Modify configuration to use remote CANcoder setting
        steer_configs.feedback.feedback_remote_sensor_id = constants.cancoder_id
        if constants.feedback_source is SteerFeedbackType.REMOTE_CANCODER:
            steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.REMOTE_CANCODER
        elif constants.feedback_source is SteerFeedbackType.FUSED_CANCODER:
            steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.FUSED_CANCODER
        elif constants.feedback_source is SteerFeedbackType.SYNC_CANCODER:
            steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.SYNC_CANCODER
        steer_configs.feedback.rotor_to_sensor_ratio = constants.steer_motor_gear_ratio

        steer_configs.motion_magic.motion_magic_cruise_velocity = 100.0 / constants.steer_motor_gear_ratio
        steer_configs.motion_magic.motion_magic_acceleration = steer_configs.motion_magic.motion_magic_cruise_velocity / 0.100
        steer_configs.motion_magic.motion_magic_expo_k_v = 0.12 * constants.steer_motor_gear_ratio
        steer_configs.motion_magic.motion_magic_expo_k_a = 1.2 / constants.steer_motor_gear_ratio

        # Enable continuous wrap for swerve modules
        steer_configs.closed_loop_general.continuous_wrap = True

        steer_configs.motor_output.inverted = (
            InvertedValue.CLOCKWISE_POSITIVE
            if constants.steer_motor_inverted
            else InvertedValue.COUNTER_CLOCKWISE_POSITIVE
        )
        response = self.steer_motor.configurator.apply(steer_configs)
        if not response.is_ok():
            print(f"TalonFX ID {self.steer_motor.device_id} failed config with error {response.name}")

        cancoder_configs = constants.cancoder_initial_configs
        cancoder_configs.magnet_sensor.magnet_offset = constants.cancoder_offset
        response = self.cancoder.configurator.apply(cancoder_configs)
        if not response.is_ok():
            print(f"CANcoder ID {self.cancoder.device_id} failed config with error {response.name}")

    @overload
    def apply(self, module_request: ModuleRequest):
        """
        Applies the desired ModuleRequest to this module.

        :param module_request: The request to apply to this module
        :type module_request:  ModuleRequest
        """
        ...

    @overload
    def apply(self, drive_request: SupportsSendRequest, steer_request: SupportsSendRequest):
        """
        Controls this module using the specified drive and steer control requests.

        This is intended only to be used for characterization of the robot; do not use this for normal use.

        :param drive_request: The control request to apply to the drive motor
        :type drive_request: SupportsSendRequest
        :param steer_request: The control request to apply to the steer motor
        :type steer_request: SupportsSendRequest
        """
        ...

    def apply(self, arg1 = None, arg2 = None):
        if isinstance(arg1, self.ModuleRequest) and arg2 is None:
            # self.apply(module_request)
            module_request = arg1

            c_state = SwerveModuleState_t()
            c_state.speed = module_request.state.speed
            c_state.angle = module_request.state.angle.radians()

            c_module_request = SwerveModuleRequest_t()
            c_module_request.state = c_state
            c_module_request.wheelForceFeedforwardX = module_request.wheel_force_feedforward_x
            c_module_request.wheelForceFeedforwardY = module_request.wheel_force_feedforward_y
            c_module_request.driveRequest = module_request.drive_request.value
            c_module_request.steerRequest = module_request.steer_request.value

            Native.api_instance().c_ctre_phoenix6_swerve_module_apply(
                self._drivetrain,
                self._module_idx,
                ctypes.byref(c_module_request),
            )
        elif arg1 is not None and arg2 is not None:
            # self.apply(drive_request, steer_request)
            drive_request: SupportsSendRequest = arg1
            steer_request: SupportsSendRequest = arg2

            self.drive_motor.set_control(drive_request.with_update_freq_hz(0))
            self.steer_motor.set_control(steer_request.with_update_freq_hz(0))
        else:
            raise TypeError('Invalid arguments for SwerveModule.apply')

    def get_position(self, refresh: bool) -> SwerveModulePosition:
        """
        Gets the state of this module and passes it back as a
        SwerveModulePosition object with latency compensated values.

        :param refresh: True if the signals should be refreshed
        :type refresh: bool
        :returns: SwerveModulePosition containing this module's state
        :rtype: SwerveModulePosition
        """
        with self._state_lock:
            c_position = Native.api_instance().c_ctre_phoenix6_swerve_module_get_position(self._drivetrain, self._module_idx, refresh)
            self._internal_state.distance = c_position.distance
            self._internal_state.angle = Rotation2d(c_position.angle)
            return self._internal_state

    def get_cached_position(self) -> SwerveModulePosition:
        """
        Gets the last cached swerve module position.
        This differs from get_position in that it will not
        perform any latency compensation or refresh the signals.

        :returns: Last cached SwerveModulePosition
        :rtype: SwerveModulePosition
        """
        with self._state_lock:
            c_position = Native.api_instance().c_ctre_phoenix6_swerve_module_get_cached_position(self._drivetrain, self._module_idx)
            self._internal_state.distance = c_position.distance
            self._internal_state.angle = Rotation2d(c_position.angle)
            return self._internal_state

    def get_current_state(self) -> SwerveModuleState:
        """
        Get the current state of the module.

        This is typically used for telemetry, as the
        SwerveModulePosition is used for odometry.

        :returns: Current state of the module
        :rtype: SwerveModuleState
        """
        with self._state_lock:
            c_state = Native.api_instance().c_ctre_phoenix6_swerve_module_get_current_state(self._drivetrain, self._module_idx)
            self._current_state.speed = c_state.speed
            self._current_state.angle = Rotation2d(c_state.angle)
            return self._current_state

    def get_target_state(self) -> SwerveModuleState:
        """
        Get the target state of the module.

        This is typically used for telemetry.

        :returns: Target state of the module
        :rtype: SwerveModuleState
        """
        with self._state_lock:
            c_state = Native.api_instance().c_ctre_phoenix6_swerve_module_get_target_state(self._drivetrain, self._module_idx)
            self._target_state.speed = c_state.speed
            self._target_state.angle = Rotation2d(c_state.angle)
            return self._target_state

    def reset_position(self):
        """
        Resets this module's drive motor position to 0 rotations.
        """
        Native.api_instance().c_ctre_phoenix6_swerve_module_reset_position(self._drivetrain, self._module_idx)

    @property
    def drive_motor(self) -> TalonFX:
        """
        Gets this module's Drive Motor TalonFX reference.

        This should be used only to access signals and change configurations that the
        swerve drivetrain does not configure itself.

        :returns: This module's Drive Motor reference
        :rtype: TalonFX
        """
        return self._drive_motor

    @property
    def steer_motor(self) -> TalonFX:
        """
        Gets this module's Steer Motor TalonFX reference.

        This should be used only to access signals and change configurations that the
        swerve drivetrain does not configure itself.

        :returns: This module's Steer Motor reference
        :rtype: TalonFX
        """
        return self._steer_motor

    @property
    def cancoder(self) -> CANcoder:
        """
        Gets this module's CANcoder reference.

        This should be used only to access signals and change configurations that the
        swerve drivetrain does not configure itself.

        :returns: This module's CANcoder reference
        :rtype: CANcoder
        """
        return self._cancoder
