"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from typing import overload, Callable
from threading import RLock
from phoenix6.status_code import StatusCode
from phoenix6.hardware.pigeon2 import Pigeon2
from phoenix6.signals.spn_enums import NeutralModeValue
from phoenix6.swerve.swerve_drivetrain_constants import SwerveDrivetrainConstants
from phoenix6.swerve.swerve_module_constants import SwerveModuleConstants
from phoenix6.swerve.swerve_module import SwerveModule
from phoenix6.swerve.utility.geometry import *
from phoenix6.swerve.utility.kinematics import *
from phoenix6.swerve import requests
from phoenix6.units import *
from phoenix6.phoenix_native import (
    Native,
    SwerveControlParams_t,
    SwerveDriveState_t,
    SwerveModulePosition_t,
    SwerveModuleState_t,
)

try:
    from wpimath.kinematics import (
        SwerveDrive2Kinematics,
        SwerveDrive3Kinematics,
        SwerveDrive4Kinematics,
        SwerveDrive6Kinematics,
    )
    from wpimath.geometry import Rotation3d

    from phoenix6.swerve.sim_swerve_drivetrain import SimSwerveDrivetrain

    USE_WPILIB = True
except ImportError:
    USE_WPILIB = False

class SwerveControlParameters:
    """
    Contains everything the control requests need to calculate the module state.
    """

    def __init__(self):
        if USE_WPILIB:
            self.kinematics: SwerveDrive2Kinematics | SwerveDrive3Kinematics | SwerveDrive4Kinematics | SwerveDrive6Kinematics = None
        self.swerve_positions: list[Translation2d] = None
        self.max_speed: meters_per_second = 0.0

        self.operator_forward_direction = Rotation2d()
        self.current_chassis_speed = ChassisSpeeds()
        self.current_pose = Pose2d()
        self.timestamp: second = 0.0
        self.update_period: second = 0.0


class SwerveDrivetrain:
    """
    Swerve Drive class utilizing CTR Electronics' Phoenix 6 API.

    This class handles the kinematics, configuration, and odometry of a
    swerve drive utilizing CTR Electronics devices. We recommend
    that users use the Swerve Mechanism Generator in Tuner X to create
    a template project that demonstrates how to use this class.

    This class will construct the hardware devices internally, so the user
    only specifies the constants (IDs, PID gains, gear ratios, etc).
    Getters for these hardware devices are available.

    If using the generator, the order in which modules are constructed is
    Front Left, Front Right, Back Left, Back Right. This means if you need
    the Back Left module, call get_module(2) to get the 3rd index
    (0-indexed) module, corresponding to the Back Left module.
    """

    class SwerveDriveState:
        """
        Plain-Old-Data class holding the state of the swerve drivetrain.
        This encapsulates most data that is relevant for telemetry or
        decision-making from the Swerve Drive.
        """

        def __init__(self):
            self.pose = Pose2d()
            """The current pose of the robot"""
            self.speeds = ChassisSpeeds()
            """The current velocity of the robot"""
            self.module_states: list[SwerveModuleState] = None
            """The current module states"""
            self.module_targets: list[SwerveModuleState] = None
            """The target module states"""
            self.module_positions: list[SwerveModulePosition] = None
            """The current module positions"""
            self.odometry_period: second = 0.0
            """The measured odometry update period, in seconds"""
            self.successful_daqs = 0
            """Number of successful data acquisitions"""
            self.failed_daqs = 0
            """Number of failed data acquisitions"""

    class OdometryThread:
        """
        Performs swerve module updates in a separate thread to minimize latency.

        :param drivetrain: ID of the swerve drivetrain
        :type drivetrain: int
        """

        def __init__(self, drivetrain: int):
            self._drivetrain = drivetrain

        def start(self):
            """
            Starts the odometry thread.
            """
            Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_odom_start(self._drivetrain)

        def stop(self):
            """
            Stops the odometry thread.
            """
            Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_odom_stop(self._drivetrain)

        def is_odometry_valid(self) -> bool:
            return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_is_odometry_valid(self._drivetrain)

        def set_thread_priority(self, priority: int):
            """
            Sets the DAQ thread priority to a real time priority under the specified priority level

            :param priority: Priority level to set the DAQ thread to.
                             This is a value between 0 and 99, with 99 indicating higher
                             priority and 0 indicating lower priority.
            :type priority: int
            """
            Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_odom_set_thread_priority(self._drivetrain, priority)

    @overload
    def __init__(self, drivetrain_constants: SwerveDrivetrainConstants, modules: list[SwerveModuleConstants]) -> None:
        """
        Constructs a CTRE SwerveDrivetrain using the specified constants.

        This constructs the underlying hardware devices, so user should not construct
        the devices themselves. If they need the devices, they can access them through
        getters in the classes.
        
        :param driveTrainConstants: Drivetrain-wide constants for the swerve drive
        :type driveTrainConstants:  SwerveDrivetrainConstants
        :param modules:             Constants for each specific module
        :type modules:              list[SwerveModuleConstants]
        """
        ...

    @overload
    def __init__(self, drivetrain_constants: SwerveDrivetrainConstants, odometry_update_frequency: hertz, modules: list[SwerveModuleConstants]) -> None:
        """
        Constructs a CTRE SwerveDrivetrain using the specified constants.

        This constructs the underlying hardware devices, so user should not construct
        the devices themselves. If they need the devices, they can access them through
        getters in the classes.
        
        :param driveTrainConstants:         Drivetrain-wide constants for the swerve drive
        :type driveTrainConstants:          SwerveDrivetrainConstants
        :param odometry_update_frequency:   The frequency to run the odometry loop. If
                                            unspecified or set to 0 Hz, this is 250 Hz on
                                            CAN FD, and 100 Hz on CAN 2.0.
        :type odometry_update_frequency:    hertz
        :param modules:                     Constants for each specific module
        :type modules:                      list[SwerveModuleConstants]
        """
        ...

    @overload
    def __init__(
        self,
        drivetrain_constants: SwerveDrivetrainConstants,
        odometry_update_frequency: hertz,
        odometry_standard_deviation: tuple[float, float, float],
        vision_standard_deviation: tuple[float, float, float],
        modules: list[SwerveModuleConstants]
    ) -> None:
        """
        Constructs a CTRE SwerveDrivetrain using the specified constants.

        This constructs the underlying hardware devices, so user should not construct
        the devices themselves. If they need the devices, they can access them through
        getters in the classes.
        
        :param driveTrainConstants:         Drivetrain-wide constants for the swerve drive
        :type driveTrainConstants:          SwerveDrivetrainConstants
        :param odometry_update_frequency:   The frequency to run the odometry loop. If
                                            unspecified or set to 0 Hz, this is 250 Hz on
                                            CAN FD, and 100 Hz on CAN 2.0.
        :type odometry_update_frequency:    hertz
        :param odometry_standard_deviation: The standard deviation for odometry calculation
        :type odometry_standard_deviation:  tuple[float, float, float]
        :param vision_standard_deviation:   The standard deviation for vision calculation
        :type vision_standard_deviation:    tuple[float, float, float]
        :param modules:                     Constants for each specific module
        :type modules:                      list[SwerveModuleConstants]
        """
        ...
    
    def __init__(
        self,
        drivetrain_constants: SwerveDrivetrainConstants,
        arg2 = None,
        arg3 = None,
        arg4 = None,
        arg5 = None,
    ):
        if (
            isinstance(arg2, list) and isinstance(arg2[0], SwerveModuleConstants) and
            arg3 is None and
            arg4 is None and
            arg5 is None
        ):
            # Self(drivetrain_constants, modules)
            modules: list[SwerveModuleConstants] = arg2

            native_drive_constants = drivetrain_constants._create_native_instance()
            native_module_constants = SwerveModuleConstants._create_native_instance(modules)

            self._drivetrain = Native.api_instance().c_ctre_phoenix6_swerve_create_drivetrain(
                native_drive_constants,
                native_module_constants,
                len(modules),
            )

            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_drive_constants, ctypes.c_char_p)))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_module_constants, ctypes.c_char_p)))
        elif (
            isinstance(arg2, (hertz, float)) and
            isinstance(arg3, list) and isinstance(arg3[0], SwerveModuleConstants) and
            arg4 is None and
            arg5 is None
        ):
            # Self(drivetrain_constants, odometry_update_frequency, modules)
            modules: list[SwerveModuleConstants] = arg3

            native_drive_constants = drivetrain_constants._create_native_instance()
            native_module_constants = SwerveModuleConstants._create_native_instance(modules)

            self._drivetrain = Native.api_instance().c_ctre_phoenix6_swerve_create_drivetrain_with_freq(
                native_drive_constants,
                arg2,
                native_module_constants,
                len(modules),
            )

            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_drive_constants, ctypes.c_char_p)))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_module_constants, ctypes.c_char_p)))
        elif (
            isinstance(arg2, (hertz, float)) and
            isinstance(arg3, tuple[float, float, float]) and
            isinstance(arg4, tuple[float, float, float]) and
            isinstance(arg5, list) and isinstance(arg5[0], SwerveModuleConstants)
        ):
            # Self(drivetrain_constants, odometry_update_frequency, odometry_standard_deviation, vision_standard_deviation, modules)
            modules: list[SwerveModuleConstants] = arg5

            odometry_standard_deviation = (ctypes.c_double * 3)()
            odometry_standard_deviation[0] = arg3[0]
            odometry_standard_deviation[1] = arg3[1]
            odometry_standard_deviation[2] = arg3[2]

            vision_standard_deviation = (ctypes.c_double * 3)()
            vision_standard_deviation[0] = arg4[0]
            vision_standard_deviation[1] = arg4[1]
            vision_standard_deviation[2] = arg4[2]

            native_drive_constants = drivetrain_constants._create_native_instance()
            native_module_constants = SwerveModuleConstants._create_native_instance(modules)

            self._drivetrain = Native.api_instance().c_ctre_phoenix6_swerve_create_drivetrain_with_freq(
                native_drive_constants,
                arg2,
                odometry_standard_deviation,
                vision_standard_deviation,
                native_module_constants,
                len(modules),
            )

            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_drive_constants, ctypes.c_char_p)))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_module_constants, ctypes.c_char_p)))
        else:
            raise TypeError('Invalid arguments for SwerveDrivetrain.__init__')

        self._modules: list[SwerveModule] = []
        self._module_locations: list[Translation2d] = []
        for i, module in enumerate(modules):
            self._modules.append(SwerveModule(module, drivetrain_constants.can_bus_name, self._drivetrain, i))
            self._module_locations.append(Translation2d(module.location_x, module.location_y))

        if USE_WPILIB:
            if len(modules) == 2:
                self._kinematics = SwerveDrive2Kinematics(self._module_locations[0], self._module_locations[1])
            elif len(modules) == 3:
                self._kinematics = SwerveDrive3Kinematics(self._module_locations[0], self._module_locations[1], self._module_locations[2])
            elif len(modules) == 4:
                self._kinematics = SwerveDrive4Kinematics(self._module_locations[0], self._module_locations[1], self._module_locations[2], self._module_locations[3])
            elif len(modules) == 6:
                self._kinematics = SwerveDrive6Kinematics(self._module_locations[0], self._module_locations[1], self._module_locations[2], self._module_locations[3], self._module_locations[4], self._module_locations[5])
            else:
                self._kinematics = None

        self._control_params = SwerveControlParameters()
        if USE_WPILIB:
            self._control_params.kinematics = self._kinematics
        self._control_params.swerve_positions = self._module_locations

        self._swerve_request: requests.SwerveRequest = requests.Idle()
        self._control_handle = None

        self._telemetry_function: Callable[['SwerveDrivetrain.SwerveDriveState'], None] = None
        self._telemetry_handle = None

        self._state_lock = RLock()
        self._cached_state = self.SwerveDriveState()
        self._cached_state.module_states = [SwerveModuleState() for _ in modules]
        self._cached_state.module_targets = [SwerveModuleState() for _ in modules]
        self._cached_state.module_positions = [SwerveModulePosition() for _ in modules]

        self._pigeon2 = Pigeon2(drivetrain_constants.pigeon2_id, drivetrain_constants.can_bus_name)
        if USE_WPILIB:
            self._sim_drive = SimSwerveDrivetrain(self._module_locations, self._pigeon2.sim_state, modules)

        if drivetrain_constants.pigeon2_configs is not None:
            retval = self.pigeon2.configurator.apply(drivetrain_constants.pigeon2_configs)
            if not retval.is_ok():
                print(f"Pigeon2 ID {self.pigeon2.device_id} failed to config with error: {retval.name}")

        # do not start thread until after applying Pigeon 2 configs
        self._odometry_thread = self.OdometryThread(self._drivetrain)
        self._odometry_thread.start()

    def __enter__(self) -> 'SwerveDrivetrain':
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        """
        Closes this SwerveDrivetrain instance.
        """
        Native.instance().c_ctre_phoenix6_swerve_destroy_drivetrain(self._drivetrain)
        self._drivetrain = 0

    if USE_WPILIB:
        def update_sim_state(self, dt: second, supply_voltage: volt):
            """
            Updates all the simulation state variables for this
            drivetrain class. User provides the update variables for the simulation.
            
            :param dt: time since last update call
            :type dt: second
            :param supply_voltage: voltage as seen at the motor controllers
            :type supply_voltage: volt
            """

            self._sim_drive.update(dt, supply_voltage, self._modules)

    @property
    def daq_thread(self) -> OdometryThread:
        """
        Gets a reference to the data acquisition thread.

        :returns: DAQ thread
        :rtype: OdometryThread
        """
        return self._odometry_thread

    def set_control(self, request: requests.SwerveRequest):
        """
        Applies the specified control request to this swerve drivetrain.

        :param request: Request to apply
        :type request: requests.SwerveRequest
        """
        if self._swerve_request is not request:
            self._swerve_request = request

            if request is None:
                Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control(self._drivetrain, None, None)
                self._control_handle = None
            elif isinstance(request, requests.NativeSwerveRequest):
                request._apply_native(self._drivetrain)
                self._control_handle = None
            else:
                def control_callback(_, control_params_ptr: ctypes._Pointer):
                    control_params: SwerveControlParams_t = control_params_ptr.contents

                    self._control_params.max_speed = control_params.kMaxSpeedMps
                    self._control_params.operator_forward_direction = Rotation2d(control_params.operatorForwardDirection)
                    self._control_params.current_chassis_speed.vx = control_params.currentChassisSpeed.vx
                    self._control_params.current_chassis_speed.vy = control_params.currentChassisSpeed.vy
                    self._control_params.current_chassis_speed.omega = control_params.currentChassisSpeed.omega
                    self._control_params.current_pose = Pose2d(
                        control_params.currentPose.x,
                        control_params.currentPose.y,
                        Rotation2d(control_params.currentPose.theta),
                    )
                    self._control_params.timestamp = control_params.timestamp
                    self._control_params.update_period = control_params.updatePeriod

                    return request.apply(self._control_params, self._modules).value

                c_control_func_t = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, ctypes.POINTER(SwerveControlParams_t))
                c_control_func = c_control_func_t(control_callback)

                Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control(self._drivetrain, None, c_control_func)
                self._control_handle = c_control_func
        elif isinstance(request, requests.NativeSwerveRequest):
            request._apply_native(self._drivetrain)

    def config_neutral_mode(self, neutral_mode: NeutralModeValue) -> StatusCode:
        """
        Configures the neutral mode to use for all modules' drive motors.

        :param neutral_mode: The drive motor neutral mode
        :type neutral_mode: NeutralModeValue
        :returns: Status code of the first failed config call, or OK if all succeeded
        :rtype: StatusCode
        """
        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_config_neutral_mode(self._drivetrain, neutral_mode.value))

    def tare_everything(self):
        """
        Zero's this swerve drive's odometry entirely.

        This will zero the entire odometry, and place the robot at 0,0
        """
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_tare_everything(self._drivetrain)

    @overload
    def seed_field_relative(self) -> None:
        """
        Takes the current orientation of the robot and makes it X forward for
        field-relative maneuvers.
        """
        ...

    @overload
    def seed_field_relative(self, location: Pose2d) -> None:
        """
        Takes the specified location and makes it the current pose for
        field-relative maneuvers

        :param location: Pose to make the current pose
        :type location: Pose2d
        """
        ...

    def seed_field_relative(self, location: Pose2d | None = None):
        if location is None:
            # self.seed_field_relative()
            Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_seed_field_relative(self._drivetrain)
        else:
            # self.seed_field_relative(location)
            Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_seed_field_relative_to(
                self._drivetrain,
                location.x,
                location.y,
                location.rotation().radians()
            )

    def set_operator_perspective_forward(self, field_direction: Rotation2d):
        """
        Takes the ForwardReferenceValue.RedAlliance perpective direction and treats
        it as the forward direction for ForwardReferenceValue.OperatorPerspective.

        If the operator is in the Blue Alliance Station, this should be 0 degrees.
        If the operator is in the Red Alliance Station, this should be 180 degrees.

        :param field_direction: Heading indicating which direction is forward from
                                the ForwardReferenceValue.RedAlliance perspective
        :type field_direction: Rotation2d
        """
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_operator_perspective_forward(self._drivetrain, field_direction.radians())

    def is_odometry_valid(self) -> bool:
        """
        Check if the odometry is currently valid

        :returns: True if odometry is valid
        :rtype: bool
        """
        return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_is_odometry_valid(self._drivetrain)

    def get_module(self, index: int) -> SwerveModule:
        """
        Get a reference to the module at the specified index.
        The index corresponds to the module described in the constructor.

        :param index: Which module to get
        :type index: int
        :returns: Reference to SwerveModule
        :rtype: SwerveModule
        """
        return self._modules[index]

    @property
    def modules(self) -> list[SwerveModule]:
        """
        Get a reference to the full array of modules.
        The indexes correspond to the module described in the constructor.

        :returns: Reference to the SwerveModule array
        :rtype: list[SwerveModule]
        """
        return self._modules

    def get_state(self) -> SwerveDriveState:
        """    
        Gets the current state of the swerve drivetrain.

        :returns: Current state of the drivetrain
        :rtype: SwerveDriveState
        """
        c_module_states = (SwerveModuleState_t * len(self._modules))()
        c_module_targets = (SwerveModuleState_t * len(self._modules))()
        c_module_positions = (SwerveModulePosition_t * len(self._modules))()

        c_state = SwerveDriveState_t()
        c_state.moduleStates = c_module_states
        c_state.moduleTargets = c_module_targets
        c_state.modulePositions = c_module_positions
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_get_state(self._drivetrain, ctypes.byref(c_state))

        with self._state_lock:
            self._cached_state.pose = Pose2d(c_state.pose.x, c_state.pose.y, Rotation2d(c_state.pose.theta))
            self._cached_state.speeds = ChassisSpeeds(c_state.speeds.vx, c_state.speeds.vy, c_state.speeds.omega)
            for i, module_state in enumerate(self._cached_state.module_states):
                module_state.speed = c_module_states[i].speed
                module_state.angle = Rotation2d(c_module_states[i].angle)
            for i, module_target in enumerate(self._cached_state.module_targets):
                module_target.speed = c_module_targets[i].speed
                module_target.angle = Rotation2d(c_module_targets[i].angle)
            for i, module_position in enumerate(self._cached_state.module_positions):
                module_position.distance = c_module_positions[i].distance
                module_position.angle = Rotation2d(c_module_positions[i].angle)
            self._cached_state.odometry_period = c_state.odometryPeriod
            self._cached_state.successful_daqs = c_state.successfulDaqs
            self._cached_state.failed_daqs = c_state.failedDaqs

            return self._cached_state

    def add_vision_measurement(self, vision_robot_pose: Pose2d, timestamp: second, vision_measurement_std_devs: tuple[float, float, float] | None = None):
        """
        Adds a vision measurement to the Kalman Filter. This will correct the
        odometry pose estimate while still accounting for measurement noise.

        This method can be called as infrequently as you want, as long as you are
        calling SwerveDrivePoseEstimator.update every loop.

        To promote stability of the pose estimate and make it robust to bad vision
        data, we recommend only adding vision measurements that are already within
        one meter or so of the current pose estimate.

        Note that the vision measurement standard deviations passed into this method
        will continue to apply to future measurements until a subsequent call to
        SwerveDrivePoseEstimator.setVisionMeasurementStdDevs or this method.

        :param vision_robot_pose:           The pose of the robot as measured by the vision
                                            camera.
        :type vision_robot_pose:            Pose2d
        :param timestamp:                   The timestamp of the vision measurement in
                                            seconds. Note that if you don't use your own
                                            time source by calling
                                            SwerveDrivePoseEstimator.updateWithTime
                                            then you must use a timestamp with an epoch
                                            since system startup (i.e., the epoch of this
                                            timestamp is the same epoch as
                                            utils.get_current_time_seconds).
                                            This means that you should use
                                            utils.get_current_time_seconds
                                            as your time source or sync the epochs.
                                            An FPGA timestamp can be converted to the correct
                                            timebase using utils.fpga_to_current_time.
        :type timestamp:                    second
        :param vision_measurement_std_devs: Standard deviations of the vision pose
                                            measurement (x position in meters, y
                                            position in meters, and heading in radians).
                                            Increase these numbers to trust the vision
                                            pose measurement less.
        :type vision_measurement_std_devs:  tuple[float, float, float] | None
        """
        if vision_measurement_std_devs is not None:
            c_vision_measurement_std_devs = (ctypes.c_double * 3)()
            c_vision_measurement_std_devs[0] = vision_measurement_std_devs[0]
            c_vision_measurement_std_devs[1] = vision_measurement_std_devs[1]
            c_vision_measurement_std_devs[2] = vision_measurement_std_devs[2]

            return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_add_vision_measurement_with_stddev(
                self._drivetrain,
                vision_robot_pose.x,
                vision_robot_pose.y,
                vision_robot_pose.rotation().radians(),
                timestamp,
                c_vision_measurement_std_devs,
            )
        else:
            return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_add_vision_measurement(
                self._drivetrain,
                vision_robot_pose.x,
                vision_robot_pose.y,
                vision_robot_pose.rotation().radians(),
                timestamp,
            )

    def set_vision_measurement_std_devs(self, vision_measurement_std_devs: tuple[float, float, float]):
        """
        Sets the pose estimator's trust of global measurements. This might be used to
        change trust in vision measurements after the autonomous period, or to change
        trust as distance to a vision target increases.

        :param vision_measurement_std_devs: Standard deviations of the vision
                                            measurements. Increase these numbers to
                                            trust global measurements from vision less.
                                            This matrix is in the form [x, y, theta]ᵀ,
                                            with units in meters and radians.
        :type vision_measurement_std_devs:  tuple[float, float, float]
        """
        c_vision_measurement_std_devs = (ctypes.c_double * 3)()
        c_vision_measurement_std_devs[0] = vision_measurement_std_devs[0]
        c_vision_measurement_std_devs[1] = vision_measurement_std_devs[1]
        c_vision_measurement_std_devs[2] = vision_measurement_std_devs[2]

        return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_vision_measurement_stddevs(self._drivetrain, c_vision_measurement_std_devs)

    def register_telemetry(self, telemetry_function: Callable[[SwerveDriveState], None]):
        """
        Register the specified lambda to be executed whenever our SwerveDriveState function
        is updated in our odometry thread.

        It is imperative that this function is cheap, as it will be executed along with
        the odometry call, and if this takes a long time, it may negatively impact
        the odometry of this stack.

        This can also be used for logging data if the function performs logging instead of telemetry
        
        :param telemetry_function: Function to call for telemetry or logging
        :type telemetry_function: Callable[[SwerveDriveState], None]
        """
        if self._telemetry_function is not telemetry_function:
            self._telemetry_function = telemetry_function

            if telemetry_function is None:
                Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_register_telemetry(self._drivetrain, None)
                self._telemetry_handle = None
            else:
                def telem_callback(_, state_ptr: ctypes._Pointer):
                    with self._state_lock:
                        state: SwerveDriveState_t = state_ptr.contents

                        self._cached_state.pose = Pose2d(state.pose.x, state.pose.y, Rotation2d(state.pose.theta))
                        self._cached_state.speeds.vx = state.speeds.vx
                        self._cached_state.speeds.vy = state.speeds.vy
                        self._cached_state.speeds.omega = state.speeds.omega
                        for i, module_state in enumerate(self._cached_state.module_states):
                            module_state.speed = state.moduleStates[i].speed
                            module_state.angle = Rotation2d(state.moduleStates[i].angle)
                        for i, module_target in enumerate(self._cached_state.module_targets):
                            module_target.speed = state.moduleTargets[i].speed
                            module_target.angle = Rotation2d(state.moduleTargets[i].angle)
                        for i, module_position in enumerate(self._cached_state.module_positions):
                            module_position.distance = state.modulePositions[i].distance
                            module_position.angle = Rotation2d(state.modulePositions[i].angle)
                        self._cached_state.odometry_period = state.odometryPeriod
                        self._cached_state.successful_daqs = state.successfulDaqs
                        self._cached_state.failed_daqs = state.failedDaqs

                        telemetry_function(self._cached_state)

                c_telem_func_t = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(SwerveDriveState_t))
                c_telem_func = c_telem_func_t(telem_callback)

                Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_register_telemetry(self._drivetrain, None, c_telem_func)
                self._telemetry_handle = c_telem_func

    if USE_WPILIB:
        def get_rotation3d(self) -> Rotation3d:
            """
            Gets the current orientation of the robot as a Rotation3d from
            the Pigeon 2 quaternion values.

            :returns: The robot orientation as a Rotation3d
            :rtype: Rotation3d
            """
            return self.pigeon2.getRotation3d()

    @property
    def pigeon2(self) -> Pigeon2:
        """
        Gets this drivetrain's Pigeon 2 reference.

        This should be used only to access signals and change configurations that the
        swerve drivetrain does not configure itself.

        :returns: This drivetrain's Pigeon 2 reference
        :rtype: Pigeon2
        """
        return self._pigeon2
