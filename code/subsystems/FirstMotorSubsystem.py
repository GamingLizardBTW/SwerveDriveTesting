import logging
log = logging.Logger('P212-robot')
import wpilib
import commands2
import phoenix6
import wpimath.controller
import wpimath.trajectory
from phoenix6.controls import VoltageOut, MotionMagicVoltage
from phoenix6 import configs


from constants import ELEC, SW


class FirstMotorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:


        self.first_motor = phoenix6.hardware.TalonFX(ELEC.first_motor_CAN_ID)
        #self.my_motor.setNeutralMode(self.brakemode)

        # Motion Magic control request
        self.motion_magic = MotionMagicVoltage(0)
        config = configs.TalonFXConfiguration()

        # Gear ratio
        config.feedback.sensor_to_mechanism_ratio = SW.First_Gear_Ratio

        # Motion Magic parameters
        config.motion_magic.motion_magic_cruise_velocity = SW.First_Cruise_Velocity
        config.motion_magic.motion_magic_acceleration = SW.First_Acceleration
        config.motion_magic.motion_magic_jerk = SW.First_Jerk

        slot0 = config.slot0
        slot0.k_s = SW.First_ks
        slot0.k_v = SW.First_kv
        slot0.k_a = SW.First_ka
        slot0.k_p = SW.First_kp
        slot0.k_i = SW.First_ki
        slot0.k_d = SW.First_kd
        
        self.first_motor.configurator.apply(config)

        
        

    def go_forward(self):
        self.first_motor.set(ELEC.first_motor_forward)

    def go_reverse(self):
        self.first_motor.set(ELEC.first_motor_reverse)

    def stop(self):
 
        self.first_motor.set(ELEC.first_motor_stop)

    def firstmotorPID(self, target):

        self.first_motor.set_control(self.motion_magic.with_position(target).with_slot(0))


    def periodic(self):
        #Position in degrees
        rotations = self.first_motor.get_rotor_position().value
        degrees = rotations * 360.0
        wrapped = degrees % 360.0
        
        #speed
        velocity = self.first_motor.get_velocity().value

        wpilib.SmartDashboard.putNumber("First Motor Rotations", rotations)
        wpilib.SmartDashboard.putNumber("First Motor Position", wrapped)
        wpilib.SmartDashboard.putNumber("First Motor Velocity", velocity)
