"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

try:
    from wpilib import MotorSafety
    from wpilib.interfaces import MotorController

    class MotorSafetyImplem(MotorSafety):
        """
        Implem of MotorSafety interface from WPILib. This allows
        late/lazy construction of WPILib's motor safety object.

        :param motor_controller: Motor Controller to implement motor safety on
        :type motor_controller: MotorController
        :param description: Description of motor controller
        :type description: str
        """
        def __init__(self, motor_controller: MotorController, description: str):
            self.__motor_controller = motor_controller
            self.__description = description

        def stopMotor(self):
            """
            Stops the controller
            """
            self.__motor_controller.stopMotor()

        def getDescription(self) -> str:
            """
            :returns: Description of motor controller
            :rtype: str
            """
            return self.__description

except ImportError:
    pass
