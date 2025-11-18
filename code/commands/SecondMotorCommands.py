import logging
logger = logging.getLogger("secondmotorsubsystemlogger")

import commands2
import wpilib
from wpilib import PS5Controller
from constants import OP  
from subsystems.SecondMotorSubsystem import SecondMotorSubsystemClass


class TriggerSpin(commands2.Command):

    def __init__(self, secondmotorsubsystem: SecondMotorSubsystemClass, controller: PS5Controller) -> None:
        super().__init__()
        self.secondmotorsub = secondmotorsubsystem
        self.controller = controller
        self.addRequirements(self.secondmotorsub)

    def initialize(self):
        logger.info("TriggerSpin Command Initialized")

    def execute(self):
        right = self.controller.getR2Axis()  # 0.0 → 1.0
        left = self.controller.getL2Axis()   # 0.0 → 1.0
        speed = right - left                  # -1.0 → +1.0
        self.secondmotorsub.run(speed)

    def end(self, interrupted: bool):
        self.secondmotorsub.stop()
        logger.info("TriggerSpin Command Ended")

    def isFinished(self):
        return False


class DisplayEncoderValue(commands2.Command):

    def __init__(self, secondmotorsubsystem: SecondMotorSubsystemClass):
        super().__init__()
        self.secondmotorsub = secondmotorsubsystem
        self.addRequirements(self.secondmotorsub)

    def initialize(self):
        wrapped_degrees = self.secondmotorsub.get_encoder_position()
        raw_rotations = self.secondmotorsub.second_motor.get_rotor_position().value
        wpilib.SmartDashboard.putNumber("Encoder Degrees (Wrapped)", wrapped_degrees)
        wpilib.SmartDashboard.putNumber("Encoder Rotations (Raw)", raw_rotations)

    def isFinished(self):
        return True


class MoveToPosition(commands2.Command):

    def __init__(self, secondmotorsubsystem: SecondMotorSubsystemClass, target_rotations: float):
        super().__init__()
        self.secondmotorsub = secondmotorsubsystem
        self.target = target_rotations
        self.addRequirements(self.secondmotorsub)

    def initialize(self):
        logger.info("MoveToPosition Command Initialized")
        self.secondmotorsub.go_to_position(self.target)

    def isFinished(self):
        return True
