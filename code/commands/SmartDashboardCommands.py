import logging
logger = logging.getLogger("firstmotorsubsystemlogger")

import wpilib
import commands2
import constants
from constants import OP



from subsystems.SmartDashboardSubsystem import SmartDashboardlSubsystemClass


class  IncrementNumber(commands2.Command):

    def __init__(self, smartdashboardsubsystem: SmartDashboardlSubsystemClass) -> None:

        self.smartdashboardsub.increment_number()
        current_value = self.smartdashboardsub.get_number()
        wpilib.SmartDashboard.putNumber("My Stored Number", current_value)

        self.smartdashboardsub = smartdashboardsubsystem
        self.addRequirements(self.smartdashboardsub)


    #def execute(self):
        
        #self.motorsub.go_forward
        #logger.info("Forward Command Running")

    def isFinished(self):

        return True

    #def end(self, interrupted: bool):

        #self.motorsub.stop()