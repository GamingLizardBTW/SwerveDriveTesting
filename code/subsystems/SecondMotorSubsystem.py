import logging
log = logging.Logger('P212-robot')

import commands2
import phoenix6
from phoenix6.controls import VoltageOut, MotionMagicVoltage
from phoenix6 import configs
import wpilib

from constants import ELEC, SW, MECH


class SecondMotorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        super().__init__()

        self.second_motor = phoenix6.hardware.TalonFX(ELEC.second_motor_CAN_ID)
        self.limit_switch = wpilib.DigitalInput(ELEC.limit_switch_port)
        self.is_limit_pressed = lambda: self.limit_switch.get()

        self.request = VoltageOut(0)

        


    def run(self, speed: float):

        if speed > 0 and not self.is_limit_pressed():
            speed = 0.0

        self.second_motor.set_control(
            self.request.with_output(speed * 12.0)
        )

    def go_forward(self):
        self.run(1.0)

    def go_reverse(self):
        self.run(-1.0)

    def stop(self):
        self.run(0.0)

    def get_encoder_position(self) -> float:

        rotations = self.second_motor.get_rotor_position().value
        degrees = rotations * 360.0
        wrapped = degrees % 360.0
        return wrapped
    

