import logging
log = logging.Logger('P212-robot')
import wpilib
import commands2
import phoenix6
import wpimath.controller
import wpimath.trajectory

from constants import ELEC


class SmartDashboardlSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        
        #self.get_number = lambda: self.stored_number()
        self.stored_number = 0
        

    def increment_number(self):
        self.stored_number = self.stored_number + 1

    def get_number(self):
        return self.stored_number

