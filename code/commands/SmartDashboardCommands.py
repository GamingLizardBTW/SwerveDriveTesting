import logging
logger = logging.getLogger("smartdashboardsubsystemlogger")

import wpilib
import commands2
import constants
from constants import OP



from subsystems.SmartDashboardSubsystem import SmartDashboardSubsystemClass


class  IncrementNumber(commands2.Command):

    def __init__(self, smartdashboardsubsystem: SmartDashboardSubsystemClass) -> None:
        super().__init__()
        self.smartdashboardsub = smartdashboardsubsystem
        self.addRequirements(self.smartdashboardsub)


    def initialize(self):
        self.smartdashboardsub.increment_number()
        current_value = self.smartdashboardsub.get_number()
        wpilib.SmartDashboard.putNumber("Stored Number", current_value)
        logger.info("Increment number command initialized")



    def isFinished(self):

        return True