"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from enum import Enum
from phoenix6.configs import (
    CANcoderConfiguration,
    Slot0Configs,
    TalonFXConfiguration,
)
from phoenix6.units import *
from phoenix6.phoenix_native import Native

class ClosedLoopOutputType(Enum):
    """
    Supported closed-loop output types.
    """

    VOLTAGE = 0
    TORQUE_CURRENT_FOC = 1
    """Requires Pro"""


class SteerFeedbackType(Enum):
    """
    Supported feedback sensors for the steer motors.
    """

    FUSED_CANCODER = 0
    """
    Requires Pro; Use FeedbackSensorSourceValue.FUSED_CANCODER
    for the steer motor.
    """
    SYNC_CANCODER = 1
    """
    Requires Pro; Use FeedbackSensorSourceValue.SYNC_CANCODER
    for the steer motor.
    """
    REMOTE_CANCODER = 2
    """
    Use FeedbackSensorSourceValue.REMOTE_CANCODER for
    the steer motor.
    """

class SwerveModuleConstants:
    """
    All constants for a swerve module.
    """

    def __init__(self):
        self.steer_motor_id: int = 0
        """
        CAN ID of the steer motor.
        """
        self.drive_motor_id: int = 0
        """
        CAN ID of the drive motor.
        """
        self.cancoder_id: int = 0
        """
        CAN ID of the CANcoder used for azimuth.
        """
        self.cancoder_offset: rotation = 0
        """
        Offset of the CANcoder.
        """
        self.location_x: meter = 0
        """
        The location of this module's wheels relative to the physical center of the
        robot in meters along the X axis of the robot.
        """
        self.location_y: meter = 0
        """
        The location of this module's wheels relative to the physical center of the
        robot in meters along the Y axis of the robot.
        """
        self.drive_motor_inverted: bool = False
        """
        True if the drive motor is inverted.
        """
        self.steer_motor_inverted: bool = False
        """
        True if the steer motor is inverted from the CANcoder.
        """
        self.drive_motor_gear_ratio: float = 0
        """
        Gear ratio between the drive motor and the wheel.
        """
        self.steer_motor_gear_ratio: float = 0
        """
        Gear ratio between the steer motor and the CANcoder. For example, the SDS Mk4
        has a steering ratio of 12.8.
        """
        self.coupling_gear_ratio: float = 0
        """
        Coupled gear ratio between the CANcoder and the drive motor.
        
        For a typical swerve module, the azimuth turn motor also drives the wheel a
        nontrivial amount, which affects the accuracy of odometry and control. This
        ratio represents the number of rotations of the drive motor caused by a rotation
        of the azimuth.
        """
        self.wheel_radius: meter = 0
        """
        Radius of the driving wheel in meters.
        """
        self.steer_motor_gains: Slot0Configs = Slot0Configs()
        """
        The steer motor closed-loop gains.
        
        The steer motor uses the control ouput type specified by
        SteerMotorClosedLoopOutput and any SwerveModule.SteerRequestType.
        """
        self.drive_motor_gains: Slot0Configs = Slot0Configs()
        """
        The drive motor closed-loop gains.
        
        When using closed-loop control, the drive motor uses the control output type
        specified by DriveMotorClosedLoopOutput and any closed-loop
        SwerveModule.DriveRequestType.
        """
        self.steer_motor_closed_loop_output: ClosedLoopOutputType = ClosedLoopOutputType.VOLTAGE
        """
        The closed-loop output type to use for the steer motors.
        """
        self.drive_motor_closed_loop_output: ClosedLoopOutputType = ClosedLoopOutputType.VOLTAGE
        """
        The closed-loop output type to use for the drive motors.
        """
        self.slip_current: ampere = 120
        """
        The maximum amount of stator current the drive motors can apply without
        slippage.
        """
        self.speed_at12_volts: meters_per_second = 0
        """
        When using open-loop drive control, this specifies the speed at which the robot
        travels when driven with 12 volts. This is used to approximate the output for a
        desired velocity. If using closed loop control, this value is ignored.
        """
        self.feedback_source: SteerFeedbackType = SteerFeedbackType.FUSED_CANCODER
        """
        Choose how the feedback sensors should be configured.
        
        If the robot does not support Pro, then this should be set to RemoteCANcoder.
        Otherwise, users have the option to use either FusedCANcoder or SyncCANcoder
        depending on if there is a risk that the CANcoder can fail in a way to provide
        "good" data.
        
        If this is set to FusedCANcoder or SyncCANcoder when the steer motor is not
        Pro-licensed, the device will automatically fall back to RemoteCANcoder and
        report a UsingProFeatureOnUnlicensedDevice status code.
        """
        self.drive_motor_initial_configs: TalonFXConfiguration = TalonFXConfiguration()
        """
        The initial configs used to configure the drive motor of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MotorOutputConfigs.NeutralMode (Brake mode, overwritten with
              SwerveDrivetrain.config_neutral_mode)
            - MotorOutputConfigs.Inverted (SwerveModuleConstants.DriveMotorInverted)
            - Slot0Configs (SwerveModuleConstants.DriveMotorGains)
            - CurrentLimitsConfigs.StatorCurrentLimit /
              TorqueCurrentConfigs.PeakForwardTorqueCurrent /
              TorqueCurrentConfigs.PeakReverseTorqueCurrent
              (SwerveModuleConstants.SlipCurrent)
            - CurrentLimitsConfigs.StatorCurrentLimitEnable (Enabled)
        
        """
        self.steer_motor_initial_configs: TalonFXConfiguration = TalonFXConfiguration()
        """
        The initial configs used to configure the steer motor of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MotorOutputConfigs.NeutralMode (Brake mode)
            - MotorOutputConfigs.Inverted (SwerveModuleConstants.SteerMotorInverted)
            - Slot0Configs (SwerveModuleConstants.SteerMotorGains)
            - FeedbackConfigs.FeedbackRemoteSensorID (SwerveModuleConstants.CANcoderId)
            - FeedbackConfigs.FeedbackSensorSource
              (SwerveModuleConstants.FeedbackSource)
            - FeedbackConfigs.RotorToSensorRatio
              (SwerveModuleConstants.SteerMotorGearRatio)
            - MotionMagicConfigs (Calculated from gear ratios)
            - ClosedLoopGeneralConfigs.ContinuousWrap (true)
        
        """
        self.cancoder_initial_configs: CANcoderConfiguration = CANcoderConfiguration()
        """
        The initial configs used to configure the CANcoder of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MagnetSensorConfigs.MagnetOffset (SwerveModuleConstants.CANcoderOffset)
        
        """
        self.steer_inertia: kilogram_square_meter = 0.00001
        """
        Simulated azimuthal inertia.
        """
        self.drive_inertia: kilogram_square_meter = 0.001
        """
        Simulated drive inertia.
        """
        self.steer_friction_voltage: volt = 0.25
        """
        Simulated steer voltage required to overcome friction.
        """
        self.drive_friction_voltage: volt = 0.25
        """
        Simulated drive voltage required to overcome friction.
        """
    
    def with_steer_motor_id(self, new_steer_motor_id: int) -> 'SwerveModuleConstants':
        """
        Modifies the steer_motor_id parameter and returns itself.
    
        CAN ID of the steer motor.
    
        :param new_steer_motor_id: Parameter to modify
        :type new_steer_motor_id: int
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.steer_motor_id = new_steer_motor_id
        return self
    
    
    def with_drive_motor_id(self, new_drive_motor_id: int) -> 'SwerveModuleConstants':
        """
        Modifies the drive_motor_id parameter and returns itself.
    
        CAN ID of the drive motor.
    
        :param new_drive_motor_id: Parameter to modify
        :type new_drive_motor_id: int
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.drive_motor_id = new_drive_motor_id
        return self
    
    
    def with_cancoder_id(self, new_cancoder_id: int) -> 'SwerveModuleConstants':
        """
        Modifies the cancoder_id parameter and returns itself.
    
        CAN ID of the CANcoder used for azimuth.
    
        :param new_cancoder_id: Parameter to modify
        :type new_cancoder_id: int
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.cancoder_id = new_cancoder_id
        return self
    
    
    def with_cancoder_offset(self, new_cancoder_offset: rotation) -> 'SwerveModuleConstants':
        """
        Modifies the cancoder_offset parameter and returns itself.
    
        Offset of the CANcoder.
    
        :param new_cancoder_offset: Parameter to modify
        :type new_cancoder_offset: rotation
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.cancoder_offset = new_cancoder_offset
        return self
    
    
    def with_location_x(self, new_location_x: meter) -> 'SwerveModuleConstants':
        """
        Modifies the location_x parameter and returns itself.
    
        The location of this module's wheels relative to the physical center of the
        robot in meters along the X axis of the robot.
    
        :param new_location_x: Parameter to modify
        :type new_location_x: meter
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.location_x = new_location_x
        return self
    
    
    def with_location_y(self, new_location_y: meter) -> 'SwerveModuleConstants':
        """
        Modifies the location_y parameter and returns itself.
    
        The location of this module's wheels relative to the physical center of the
        robot in meters along the Y axis of the robot.
    
        :param new_location_y: Parameter to modify
        :type new_location_y: meter
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.location_y = new_location_y
        return self
    
    
    def with_drive_motor_inverted(self, new_drive_motor_inverted: bool) -> 'SwerveModuleConstants':
        """
        Modifies the drive_motor_inverted parameter and returns itself.
    
        True if the drive motor is inverted.
    
        :param new_drive_motor_inverted: Parameter to modify
        :type new_drive_motor_inverted: bool
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.drive_motor_inverted = new_drive_motor_inverted
        return self
    
    
    def with_steer_motor_inverted(self, new_steer_motor_inverted: bool) -> 'SwerveModuleConstants':
        """
        Modifies the steer_motor_inverted parameter and returns itself.
    
        True if the steer motor is inverted from the CANcoder.
    
        :param new_steer_motor_inverted: Parameter to modify
        :type new_steer_motor_inverted: bool
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.steer_motor_inverted = new_steer_motor_inverted
        return self
    
    
    def with_drive_motor_gear_ratio(self, new_drive_motor_gear_ratio: float) -> 'SwerveModuleConstants':
        """
        Modifies the drive_motor_gear_ratio parameter and returns itself.
    
        Gear ratio between the drive motor and the wheel.
    
        :param new_drive_motor_gear_ratio: Parameter to modify
        :type new_drive_motor_gear_ratio: float
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.drive_motor_gear_ratio = new_drive_motor_gear_ratio
        return self
    
    
    def with_steer_motor_gear_ratio(self, new_steer_motor_gear_ratio: float) -> 'SwerveModuleConstants':
        """
        Modifies the steer_motor_gear_ratio parameter and returns itself.
    
        Gear ratio between the steer motor and the CANcoder. For example, the SDS Mk4
        has a steering ratio of 12.8.
    
        :param new_steer_motor_gear_ratio: Parameter to modify
        :type new_steer_motor_gear_ratio: float
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.steer_motor_gear_ratio = new_steer_motor_gear_ratio
        return self
    
    
    def with_coupling_gear_ratio(self, new_coupling_gear_ratio: float) -> 'SwerveModuleConstants':
        """
        Modifies the coupling_gear_ratio parameter and returns itself.
    
        Coupled gear ratio between the CANcoder and the drive motor.
        
        For a typical swerve module, the azimuth turn motor also drives the wheel a
        nontrivial amount, which affects the accuracy of odometry and control. This
        ratio represents the number of rotations of the drive motor caused by a rotation
        of the azimuth.
    
        :param new_coupling_gear_ratio: Parameter to modify
        :type new_coupling_gear_ratio: float
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.coupling_gear_ratio = new_coupling_gear_ratio
        return self
    
    
    def with_wheel_radius(self, new_wheel_radius: meter) -> 'SwerveModuleConstants':
        """
        Modifies the wheel_radius parameter and returns itself.
    
        Radius of the driving wheel in meters.
    
        :param new_wheel_radius: Parameter to modify
        :type new_wheel_radius: meter
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.wheel_radius = new_wheel_radius
        return self
    
    
    def with_steer_motor_gains(self, new_steer_motor_gains: Slot0Configs) -> 'SwerveModuleConstants':
        """
        Modifies the steer_motor_gains parameter and returns itself.
    
        The steer motor closed-loop gains.
        
        The steer motor uses the control ouput type specified by
        SteerMotorClosedLoopOutput and any SwerveModule.SteerRequestType.
    
        :param new_steer_motor_gains: Parameter to modify
        :type new_steer_motor_gains: Slot0Configs
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.steer_motor_gains = new_steer_motor_gains
        return self
    
    
    def with_drive_motor_gains(self, new_drive_motor_gains: Slot0Configs) -> 'SwerveModuleConstants':
        """
        Modifies the drive_motor_gains parameter and returns itself.
    
        The drive motor closed-loop gains.
        
        When using closed-loop control, the drive motor uses the control output type
        specified by DriveMotorClosedLoopOutput and any closed-loop
        SwerveModule.DriveRequestType.
    
        :param new_drive_motor_gains: Parameter to modify
        :type new_drive_motor_gains: Slot0Configs
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.drive_motor_gains = new_drive_motor_gains
        return self
    
    
    def with_steer_motor_closed_loop_output(self, new_steer_motor_closed_loop_output: ClosedLoopOutputType) -> 'SwerveModuleConstants':
        """
        Modifies the steer_motor_closed_loop_output parameter and returns itself.
    
        The closed-loop output type to use for the steer motors.
    
        :param new_steer_motor_closed_loop_output: Parameter to modify
        :type new_steer_motor_closed_loop_output: ClosedLoopOutputType
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.steer_motor_closed_loop_output = new_steer_motor_closed_loop_output
        return self
    
    
    def with_drive_motor_closed_loop_output(self, new_drive_motor_closed_loop_output: ClosedLoopOutputType) -> 'SwerveModuleConstants':
        """
        Modifies the drive_motor_closed_loop_output parameter and returns itself.
    
        The closed-loop output type to use for the drive motors.
    
        :param new_drive_motor_closed_loop_output: Parameter to modify
        :type new_drive_motor_closed_loop_output: ClosedLoopOutputType
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.drive_motor_closed_loop_output = new_drive_motor_closed_loop_output
        return self
    
    
    def with_slip_current(self, new_slip_current: ampere) -> 'SwerveModuleConstants':
        """
        Modifies the slip_current parameter and returns itself.
    
        The maximum amount of stator current the drive motors can apply without
        slippage.
    
        :param new_slip_current: Parameter to modify
        :type new_slip_current: ampere
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.slip_current = new_slip_current
        return self
    
    
    def with_speed_at12_volts(self, new_speed_at12_volts: meters_per_second) -> 'SwerveModuleConstants':
        """
        Modifies the speed_at12_volts parameter and returns itself.
    
        When using open-loop drive control, this specifies the speed at which the robot
        travels when driven with 12 volts. This is used to approximate the output for a
        desired velocity. If using closed loop control, this value is ignored.
    
        :param new_speed_at12_volts: Parameter to modify
        :type new_speed_at12_volts: meters_per_second
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.speed_at12_volts = new_speed_at12_volts
        return self
    
    
    def with_feedback_source(self, new_feedback_source: SteerFeedbackType) -> 'SwerveModuleConstants':
        """
        Modifies the feedback_source parameter and returns itself.
    
        Choose how the feedback sensors should be configured.
        
        If the robot does not support Pro, then this should be set to RemoteCANcoder.
        Otherwise, users have the option to use either FusedCANcoder or SyncCANcoder
        depending on if there is a risk that the CANcoder can fail in a way to provide
        "good" data.
        
        If this is set to FusedCANcoder or SyncCANcoder when the steer motor is not
        Pro-licensed, the device will automatically fall back to RemoteCANcoder and
        report a UsingProFeatureOnUnlicensedDevice status code.
    
        :param new_feedback_source: Parameter to modify
        :type new_feedback_source: SteerFeedbackType
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.feedback_source = new_feedback_source
        return self
    
    
    def with_drive_motor_initial_configs(self, new_drive_motor_initial_configs: TalonFXConfiguration) -> 'SwerveModuleConstants':
        """
        Modifies the drive_motor_initial_configs parameter and returns itself.
    
        The initial configs used to configure the drive motor of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MotorOutputConfigs.NeutralMode (Brake mode, overwritten with
              SwerveDrivetrain.config_neutral_mode)
            - MotorOutputConfigs.Inverted (SwerveModuleConstants.DriveMotorInverted)
            - Slot0Configs (SwerveModuleConstants.DriveMotorGains)
            - CurrentLimitsConfigs.StatorCurrentLimit /
              TorqueCurrentConfigs.PeakForwardTorqueCurrent /
              TorqueCurrentConfigs.PeakReverseTorqueCurrent
              (SwerveModuleConstants.SlipCurrent)
            - CurrentLimitsConfigs.StatorCurrentLimitEnable (Enabled)
        
    
        :param new_drive_motor_initial_configs: Parameter to modify
        :type new_drive_motor_initial_configs: TalonFXConfiguration
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.drive_motor_initial_configs = new_drive_motor_initial_configs
        return self
    
    
    def with_steer_motor_initial_configs(self, new_steer_motor_initial_configs: TalonFXConfiguration) -> 'SwerveModuleConstants':
        """
        Modifies the steer_motor_initial_configs parameter and returns itself.
    
        The initial configs used to configure the steer motor of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MotorOutputConfigs.NeutralMode (Brake mode)
            - MotorOutputConfigs.Inverted (SwerveModuleConstants.SteerMotorInverted)
            - Slot0Configs (SwerveModuleConstants.SteerMotorGains)
            - FeedbackConfigs.FeedbackRemoteSensorID (SwerveModuleConstants.CANcoderId)
            - FeedbackConfigs.FeedbackSensorSource
              (SwerveModuleConstants.FeedbackSource)
            - FeedbackConfigs.RotorToSensorRatio
              (SwerveModuleConstants.SteerMotorGearRatio)
            - MotionMagicConfigs (Calculated from gear ratios)
            - ClosedLoopGeneralConfigs.ContinuousWrap (true)
        
    
        :param new_steer_motor_initial_configs: Parameter to modify
        :type new_steer_motor_initial_configs: TalonFXConfiguration
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.steer_motor_initial_configs = new_steer_motor_initial_configs
        return self
    
    
    def with_cancoder_initial_configs(self, new_cancoder_initial_configs: CANcoderConfiguration) -> 'SwerveModuleConstants':
        """
        Modifies the cancoder_initial_configs parameter and returns itself.
    
        The initial configs used to configure the CANcoder of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MagnetSensorConfigs.MagnetOffset (SwerveModuleConstants.CANcoderOffset)
        
    
        :param new_cancoder_initial_configs: Parameter to modify
        :type new_cancoder_initial_configs: CANcoderConfiguration
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.cancoder_initial_configs = new_cancoder_initial_configs
        return self
    
    
    def with_steer_inertia(self, new_steer_inertia: kilogram_square_meter) -> 'SwerveModuleConstants':
        """
        Modifies the steer_inertia parameter and returns itself.
    
        Simulated azimuthal inertia.
    
        :param new_steer_inertia: Parameter to modify
        :type new_steer_inertia: kilogram_square_meter
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.steer_inertia = new_steer_inertia
        return self
    
    
    def with_drive_inertia(self, new_drive_inertia: kilogram_square_meter) -> 'SwerveModuleConstants':
        """
        Modifies the drive_inertia parameter and returns itself.
    
        Simulated drive inertia.
    
        :param new_drive_inertia: Parameter to modify
        :type new_drive_inertia: kilogram_square_meter
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.drive_inertia = new_drive_inertia
        return self
    
    
    def with_steer_friction_voltage(self, new_steer_friction_voltage: volt) -> 'SwerveModuleConstants':
        """
        Modifies the steer_friction_voltage parameter and returns itself.
    
        Simulated steer voltage required to overcome friction.
    
        :param new_steer_friction_voltage: Parameter to modify
        :type new_steer_friction_voltage: volt
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.steer_friction_voltage = new_steer_friction_voltage
        return self
    
    
    def with_drive_friction_voltage(self, new_drive_friction_voltage: volt) -> 'SwerveModuleConstants':
        """
        Modifies the drive_friction_voltage parameter and returns itself.
    
        Simulated drive voltage required to overcome friction.
    
        :param new_drive_friction_voltage: Parameter to modify
        :type new_drive_friction_voltage: volt
        :returns: this object
        :rtype: SwerveModuleConstants
        """
    
        self.drive_friction_voltage = new_drive_friction_voltage
        return self
    
    
    @staticmethod
    def _create_native_instance(constants_list: list['SwerveModuleConstants']) -> ctypes.c_void_p:
        retval = Native.api_instance().c_ctre_phoenix6_swerve_create_module_constants_arr(len(constants_list))
        for i in range(0, len(constants_list)):
            constants = constants_list[i]
            
            Native.api_instance().c_ctre_phoenix6_swerve_set_module_constants(
                retval, i,
                constants.steer_motor_id,
                constants.drive_motor_id,
                constants.cancoder_id,
                constants.cancoder_offset,
                constants.location_x,
                constants.location_y,
                constants.drive_motor_inverted,
                constants.steer_motor_inverted,
                constants.drive_motor_gear_ratio,
                constants.steer_motor_gear_ratio,
                constants.coupling_gear_ratio,
                constants.wheel_radius,
                constants.steer_motor_closed_loop_output.value,
                constants.drive_motor_closed_loop_output.value,
                constants.slip_current,
                constants.speed_at12_volts,
                constants.feedback_source.value,
                constants.steer_inertia,
                constants.drive_inertia,
                constants.steer_friction_voltage,
                constants.drive_friction_voltage
            )
        return retval
    

class SwerveModuleConstantsFactory:
    """
    Constants that are common across the swerve modules, used for
    creating instances of module-specific SwerveModuleConstants.
    """

    def __init__(self):
        self.drive_motor_gear_ratio: float = 0
        """
        Gear ratio between the drive motor and the wheel.
        """
        self.steer_motor_gear_ratio: float = 0
        """
        Gear ratio between the steer motor and the CANcoder. For example, the SDS Mk4
        has a steering ratio of 12.8.
        """
        self.coupling_gear_ratio: float = 0
        """
        Coupled gear ratio between the CANcoder and the drive motor.
        
        For a typical swerve module, the azimuth turn motor also drives the wheel a
        nontrivial amount, which affects the accuracy of odometry and control. This
        ratio represents the number of rotations of the drive motor caused by a rotation
        of the azimuth.
        """
        self.wheel_radius: meter = 0
        """
        Radius of the driving wheel in meters.
        """
        self.steer_motor_gains: Slot0Configs = Slot0Configs()
        """
        The steer motor closed-loop gains.
        
        The steer motor uses the control ouput type specified by
        SteerMotorClosedLoopOutput and any SwerveModule.SteerRequestType.
        """
        self.drive_motor_gains: Slot0Configs = Slot0Configs()
        """
        The drive motor closed-loop gains.
        
        When using closed-loop control, the drive motor uses the control output type
        specified by DriveMotorClosedLoopOutput and any closed-loop
        SwerveModule.DriveRequestType.
        """
        self.steer_motor_closed_loop_output: ClosedLoopOutputType = ClosedLoopOutputType.VOLTAGE
        """
        The closed-loop output type to use for the steer motors.
        """
        self.drive_motor_closed_loop_output: ClosedLoopOutputType = ClosedLoopOutputType.VOLTAGE
        """
        The closed-loop output type to use for the drive motors.
        """
        self.slip_current: ampere = 120
        """
        The maximum amount of stator current the drive motors can apply without
        slippage.
        """
        self.speed_at12_volts: meters_per_second = 0
        """
        When using open-loop drive control, this specifies the speed at which the robot
        travels when driven with 12 volts. This is used to approximate the output for a
        desired velocity. If using closed loop control, this value is ignored.
        """
        self.feedback_source: SteerFeedbackType = SteerFeedbackType.FUSED_CANCODER
        """
        Choose how the feedback sensors should be configured.
        
        If the robot does not support Pro, then this should be set to RemoteCANcoder.
        Otherwise, users have the option to use either FusedCANcoder or SyncCANcoder
        depending on if there is a risk that the CANcoder can fail in a way to provide
        "good" data.
        
        If this is set to FusedCANcoder or SyncCANcoder when the steer motor is not
        Pro-licensed, the device will automatically fall back to RemoteCANcoder and
        report a UsingProFeatureOnUnlicensedDevice status code.
        """
        self.drive_motor_initial_configs: TalonFXConfiguration = TalonFXConfiguration()
        """
        The initial configs used to configure the drive motor of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MotorOutputConfigs.NeutralMode (Brake mode, overwritten with
              SwerveDrivetrain.config_neutral_mode)
            - MotorOutputConfigs.Inverted (SwerveModuleConstants.DriveMotorInverted)
            - Slot0Configs (SwerveModuleConstants.DriveMotorGains)
            - CurrentLimitsConfigs.StatorCurrentLimit /
              TorqueCurrentConfigs.PeakForwardTorqueCurrent /
              TorqueCurrentConfigs.PeakReverseTorqueCurrent
              (SwerveModuleConstants.SlipCurrent)
            - CurrentLimitsConfigs.StatorCurrentLimitEnable (Enabled)
        
        """
        self.steer_motor_initial_configs: TalonFXConfiguration = TalonFXConfiguration()
        """
        The initial configs used to configure the steer motor of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MotorOutputConfigs.NeutralMode (Brake mode)
            - MotorOutputConfigs.Inverted (SwerveModuleConstants.SteerMotorInverted)
            - Slot0Configs (SwerveModuleConstants.SteerMotorGains)
            - FeedbackConfigs.FeedbackRemoteSensorID (SwerveModuleConstants.CANcoderId)
            - FeedbackConfigs.FeedbackSensorSource
              (SwerveModuleConstants.FeedbackSource)
            - FeedbackConfigs.RotorToSensorRatio
              (SwerveModuleConstants.SteerMotorGearRatio)
            - MotionMagicConfigs (Calculated from gear ratios)
            - ClosedLoopGeneralConfigs.ContinuousWrap (true)
        
        """
        self.cancoder_initial_configs: CANcoderConfiguration = CANcoderConfiguration()
        """
        The initial configs used to configure the CANcoder of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MagnetSensorConfigs.MagnetOffset (SwerveModuleConstants.CANcoderOffset)
        
        """
        self.steer_inertia: kilogram_square_meter = 0.00001
        """
        Simulated azimuthal inertia.
        """
        self.drive_inertia: kilogram_square_meter = 0.001
        """
        Simulated drive inertia.
        """
        self.steer_friction_voltage: volt = 0.25
        """
        Simulated steer voltage required to overcome friction.
        """
        self.drive_friction_voltage: volt = 0.25
        """
        Simulated drive voltage required to overcome friction.
        """
    
    def with_drive_motor_gear_ratio(self, new_drive_motor_gear_ratio: float) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the drive_motor_gear_ratio parameter and returns itself.
    
        Gear ratio between the drive motor and the wheel.
    
        :param new_drive_motor_gear_ratio: Parameter to modify
        :type new_drive_motor_gear_ratio: float
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.drive_motor_gear_ratio = new_drive_motor_gear_ratio
        return self
    
    
    def with_steer_motor_gear_ratio(self, new_steer_motor_gear_ratio: float) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the steer_motor_gear_ratio parameter and returns itself.
    
        Gear ratio between the steer motor and the CANcoder. For example, the SDS Mk4
        has a steering ratio of 12.8.
    
        :param new_steer_motor_gear_ratio: Parameter to modify
        :type new_steer_motor_gear_ratio: float
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.steer_motor_gear_ratio = new_steer_motor_gear_ratio
        return self
    
    
    def with_coupling_gear_ratio(self, new_coupling_gear_ratio: float) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the coupling_gear_ratio parameter and returns itself.
    
        Coupled gear ratio between the CANcoder and the drive motor.
        
        For a typical swerve module, the azimuth turn motor also drives the wheel a
        nontrivial amount, which affects the accuracy of odometry and control. This
        ratio represents the number of rotations of the drive motor caused by a rotation
        of the azimuth.
    
        :param new_coupling_gear_ratio: Parameter to modify
        :type new_coupling_gear_ratio: float
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.coupling_gear_ratio = new_coupling_gear_ratio
        return self
    
    
    def with_wheel_radius(self, new_wheel_radius: meter) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the wheel_radius parameter and returns itself.
    
        Radius of the driving wheel in meters.
    
        :param new_wheel_radius: Parameter to modify
        :type new_wheel_radius: meter
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.wheel_radius = new_wheel_radius
        return self
    
    
    def with_steer_motor_gains(self, new_steer_motor_gains: Slot0Configs) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the steer_motor_gains parameter and returns itself.
    
        The steer motor closed-loop gains.
        
        The steer motor uses the control ouput type specified by
        SteerMotorClosedLoopOutput and any SwerveModule.SteerRequestType.
    
        :param new_steer_motor_gains: Parameter to modify
        :type new_steer_motor_gains: Slot0Configs
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.steer_motor_gains = new_steer_motor_gains
        return self
    
    
    def with_drive_motor_gains(self, new_drive_motor_gains: Slot0Configs) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the drive_motor_gains parameter and returns itself.
    
        The drive motor closed-loop gains.
        
        When using closed-loop control, the drive motor uses the control output type
        specified by DriveMotorClosedLoopOutput and any closed-loop
        SwerveModule.DriveRequestType.
    
        :param new_drive_motor_gains: Parameter to modify
        :type new_drive_motor_gains: Slot0Configs
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.drive_motor_gains = new_drive_motor_gains
        return self
    
    
    def with_steer_motor_closed_loop_output(self, new_steer_motor_closed_loop_output: ClosedLoopOutputType) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the steer_motor_closed_loop_output parameter and returns itself.
    
        The closed-loop output type to use for the steer motors.
    
        :param new_steer_motor_closed_loop_output: Parameter to modify
        :type new_steer_motor_closed_loop_output: ClosedLoopOutputType
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.steer_motor_closed_loop_output = new_steer_motor_closed_loop_output
        return self
    
    
    def with_drive_motor_closed_loop_output(self, new_drive_motor_closed_loop_output: ClosedLoopOutputType) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the drive_motor_closed_loop_output parameter and returns itself.
    
        The closed-loop output type to use for the drive motors.
    
        :param new_drive_motor_closed_loop_output: Parameter to modify
        :type new_drive_motor_closed_loop_output: ClosedLoopOutputType
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.drive_motor_closed_loop_output = new_drive_motor_closed_loop_output
        return self
    
    
    def with_slip_current(self, new_slip_current: ampere) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the slip_current parameter and returns itself.
    
        The maximum amount of stator current the drive motors can apply without
        slippage.
    
        :param new_slip_current: Parameter to modify
        :type new_slip_current: ampere
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.slip_current = new_slip_current
        return self
    
    
    def with_speed_at12_volts(self, new_speed_at12_volts: meters_per_second) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the speed_at12_volts parameter and returns itself.
    
        When using open-loop drive control, this specifies the speed at which the robot
        travels when driven with 12 volts. This is used to approximate the output for a
        desired velocity. If using closed loop control, this value is ignored.
    
        :param new_speed_at12_volts: Parameter to modify
        :type new_speed_at12_volts: meters_per_second
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.speed_at12_volts = new_speed_at12_volts
        return self
    
    
    def with_feedback_source(self, new_feedback_source: SteerFeedbackType) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the feedback_source parameter and returns itself.
    
        Choose how the feedback sensors should be configured.
        
        If the robot does not support Pro, then this should be set to RemoteCANcoder.
        Otherwise, users have the option to use either FusedCANcoder or SyncCANcoder
        depending on if there is a risk that the CANcoder can fail in a way to provide
        "good" data.
        
        If this is set to FusedCANcoder or SyncCANcoder when the steer motor is not
        Pro-licensed, the device will automatically fall back to RemoteCANcoder and
        report a UsingProFeatureOnUnlicensedDevice status code.
    
        :param new_feedback_source: Parameter to modify
        :type new_feedback_source: SteerFeedbackType
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.feedback_source = new_feedback_source
        return self
    
    
    def with_drive_motor_initial_configs(self, new_drive_motor_initial_configs: TalonFXConfiguration) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the drive_motor_initial_configs parameter and returns itself.
    
        The initial configs used to configure the drive motor of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MotorOutputConfigs.NeutralMode (Brake mode, overwritten with
              SwerveDrivetrain.config_neutral_mode)
            - MotorOutputConfigs.Inverted (SwerveModuleConstants.DriveMotorInverted)
            - Slot0Configs (SwerveModuleConstants.DriveMotorGains)
            - CurrentLimitsConfigs.StatorCurrentLimit /
              TorqueCurrentConfigs.PeakForwardTorqueCurrent /
              TorqueCurrentConfigs.PeakReverseTorqueCurrent
              (SwerveModuleConstants.SlipCurrent)
            - CurrentLimitsConfigs.StatorCurrentLimitEnable (Enabled)
        
    
        :param new_drive_motor_initial_configs: Parameter to modify
        :type new_drive_motor_initial_configs: TalonFXConfiguration
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.drive_motor_initial_configs = new_drive_motor_initial_configs
        return self
    
    
    def with_steer_motor_initial_configs(self, new_steer_motor_initial_configs: TalonFXConfiguration) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the steer_motor_initial_configs parameter and returns itself.
    
        The initial configs used to configure the steer motor of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MotorOutputConfigs.NeutralMode (Brake mode)
            - MotorOutputConfigs.Inverted (SwerveModuleConstants.SteerMotorInverted)
            - Slot0Configs (SwerveModuleConstants.SteerMotorGains)
            - FeedbackConfigs.FeedbackRemoteSensorID (SwerveModuleConstants.CANcoderId)
            - FeedbackConfigs.FeedbackSensorSource
              (SwerveModuleConstants.FeedbackSource)
            - FeedbackConfigs.RotorToSensorRatio
              (SwerveModuleConstants.SteerMotorGearRatio)
            - MotionMagicConfigs (Calculated from gear ratios)
            - ClosedLoopGeneralConfigs.ContinuousWrap (true)
        
    
        :param new_steer_motor_initial_configs: Parameter to modify
        :type new_steer_motor_initial_configs: TalonFXConfiguration
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.steer_motor_initial_configs = new_steer_motor_initial_configs
        return self
    
    
    def with_cancoder_initial_configs(self, new_cancoder_initial_configs: CANcoderConfiguration) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the cancoder_initial_configs parameter and returns itself.
    
        The initial configs used to configure the CANcoder of the swerve module. The
        default value is the factory-default.
        
        Users may change the initial configuration as they need. Any config that's not
        referenced in the SwerveModuleConstants class is available to be changed.
        
        The list of configs that will be overwritten is as follows:
        
            - MagnetSensorConfigs.MagnetOffset (SwerveModuleConstants.CANcoderOffset)
        
    
        :param new_cancoder_initial_configs: Parameter to modify
        :type new_cancoder_initial_configs: CANcoderConfiguration
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.cancoder_initial_configs = new_cancoder_initial_configs
        return self
    
    
    def with_steer_inertia(self, new_steer_inertia: kilogram_square_meter) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the steer_inertia parameter and returns itself.
    
        Simulated azimuthal inertia.
    
        :param new_steer_inertia: Parameter to modify
        :type new_steer_inertia: kilogram_square_meter
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.steer_inertia = new_steer_inertia
        return self
    
    
    def with_drive_inertia(self, new_drive_inertia: kilogram_square_meter) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the drive_inertia parameter and returns itself.
    
        Simulated drive inertia.
    
        :param new_drive_inertia: Parameter to modify
        :type new_drive_inertia: kilogram_square_meter
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.drive_inertia = new_drive_inertia
        return self
    
    
    def with_steer_friction_voltage(self, new_steer_friction_voltage: volt) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the steer_friction_voltage parameter and returns itself.
    
        Simulated steer voltage required to overcome friction.
    
        :param new_steer_friction_voltage: Parameter to modify
        :type new_steer_friction_voltage: volt
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.steer_friction_voltage = new_steer_friction_voltage
        return self
    
    
    def with_drive_friction_voltage(self, new_drive_friction_voltage: volt) -> 'SwerveModuleConstantsFactory':
        """
        Modifies the drive_friction_voltage parameter and returns itself.
    
        Simulated drive voltage required to overcome friction.
    
        :param new_drive_friction_voltage: Parameter to modify
        :type new_drive_friction_voltage: volt
        :returns: this object
        :rtype: SwerveModuleConstantsFactory
        """
    
        self.drive_friction_voltage = new_drive_friction_voltage
        return self
    
    
    def create_module_constants(
        self,
        steer_motor_id: int,
        drive_motor_id: int,
        cancoder_id: int,
        cancoder_offset: rotation,
        location_x: meter,
        location_y: meter,
        drive_motor_inverted: bool,
        steer_motor_inverted: bool
    ) -> SwerveModuleConstants:
        """
        Creates the constants for a swerve module with the given properties.
    
        :param steer_motor_id: CAN ID of the steer motor.
        :type steer_motor_id: int
        :param drive_motor_id: CAN ID of the drive motor.
        :type drive_motor_id: int
        :param cancoder_id: CAN ID of the CANcoder used for azimuth.
        :type cancoder_id: int
        :param cancoder_offset: Offset of the CANcoder.
        :type cancoder_offset: rotation
        :param location_x: The location of this module's wheels relative to the physical center of the robot in meters along the X axis of the robot.
        :type location_x: meter
        :param location_y: The location of this module's wheels relative to the physical center of the robot in meters along the Y axis of the robot.
        :type location_y: meter
        :param drive_motor_inverted: True if the drive motor is inverted.
        :type drive_motor_inverted: bool
        :param steer_motor_inverted: True if the steer motor is inverted from the CANcoder.
        :type steer_motor_inverted: bool
        :returns: Constants for the swerve module
        :rtype: SwerveModuleConstants
        """
    
        return (
            SwerveModuleConstants()
                .with_steer_motor_id(steer_motor_id)
                .with_drive_motor_id(drive_motor_id)
                .with_cancoder_id(cancoder_id)
                .with_cancoder_offset(cancoder_offset)
                .with_location_x(location_x)
                .with_location_y(location_y)
                .with_drive_motor_inverted(drive_motor_inverted)
                .with_steer_motor_inverted(steer_motor_inverted)
                .with_drive_motor_gear_ratio(self.drive_motor_gear_ratio)
                .with_steer_motor_gear_ratio(self.steer_motor_gear_ratio)
                .with_coupling_gear_ratio(self.coupling_gear_ratio)
                .with_wheel_radius(self.wheel_radius)
                .with_steer_motor_gains(self.steer_motor_gains)
                .with_drive_motor_gains(self.drive_motor_gains)
                .with_steer_motor_closed_loop_output(self.steer_motor_closed_loop_output)
                .with_drive_motor_closed_loop_output(self.drive_motor_closed_loop_output)
                .with_slip_current(self.slip_current)
                .with_speed_at12_volts(self.speed_at12_volts)
                .with_feedback_source(self.feedback_source)
                .with_drive_motor_initial_configs(self.drive_motor_initial_configs)
                .with_steer_motor_initial_configs(self.steer_motor_initial_configs)
                .with_cancoder_initial_configs(self.cancoder_initial_configs)
                .with_steer_inertia(self.steer_inertia)
                .with_drive_inertia(self.drive_inertia)
                .with_steer_friction_voltage(self.steer_friction_voltage)
                .with_drive_friction_voltage(self.drive_friction_voltage)
        )
    
