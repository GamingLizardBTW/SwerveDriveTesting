import logging
log = logging.Logger('P212-robot')

import commands2
import phoenix6
from phoenix6.controls import VoltageOut
import wpilib

from constants import ELEC


class SecondMotorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        super().__init__()
        self.second_motor = phoenix6.hardware.TalonFX(ELEC.second_motor_CAN_ID)
        self.request = VoltageOut(0)
        self.limit_switch = wpilib.DigitalInput(ELEC.limit_switch_port)
        self.is_limit_pressed = lambda: self.limit_switch.get()

    def run(self, speed: float):
        """
        speed range: -1.0 to +1.0
        """
        if speed > 0 and self.is_limit_pressed():
            # Prevent forward movement
            speed = 0.0
        self.second_motor.set_control(self.request.with_output(speed * 12.0))

    def go_forward(self):
        self.run(1.0)

    def go_reverse(self):
        self.run(-1.0)

    def stop(self):
        self.run(0.0)

    def get_encoder_position(self) -> float:

        return self.second_motor.get_rotor_position().getValue()

