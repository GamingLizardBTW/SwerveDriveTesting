import logging
logger = logging.getLogger("swervedrivesubsystemlogger")
import commands2
from wpilib import SmartDashboard
from constants import OP, SW
import math

class SwerveDriveCommand(commands2.Command):
    """
    Default command for the swerve drive.
    Reads the PS5 controller and drives the robot.
    """
    def __init__(self, swerve_subsystem, controller):
        super().__init__()
        self.swervesub = swerve_subsystem
        self.controller = controller
        self.addRequirements(swerve_subsystem)

    def initialize(self):
        logger.info("TriggerSpin Command Initialized")

    def execute(self):

        #Forward/back (invert if necessary)
        x_speed = -self.controller.getLeftY() * SW.swerve_max_speed_mps
        #Strafe
        y_speed = self.controller.getLeftX() * SW.swerve_max_speed_mps
        #Rotating
        rot_speed = self.controller.getRightX() * SW.swerve_max_angular_speed_rps

        #Drive the swerve subsystem
        self.swervesub.drive(x_speed, y_speed, rot_speed, field_relative=True)

        #Shows movement speed
        SmartDashboard.putNumber("Swerve X Speed", x_speed)
        SmartDashboard.putNumber("Swerve Y Speed", y_speed)
        SmartDashboard.putNumber("Swerve Rotation Speed", rot_speed)

    def end(self, interrupted: bool):
        self.swervesub.stop()
        logger.info("Swerve Drive Ended")

    def isFinished(self):
        return False
