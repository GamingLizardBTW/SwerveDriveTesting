import math
import wpilib
import wpimath
from wpilib import SmartDashboard
from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import SwerveDrive2Kinematics, SwerveModuleState
from phoenix6.hardware import TalonFX, CANcoder
from phoenix6.controls import PositionVoltage, VelocityVoltage
from phoenix6.configs import TalonFXConfiguration
import commands2
from constants import MECH, PHYS, ELEC


class SwerveModule:
    def __init__(self, drive_motor_id, steer_motor_id, encoder_id, angle_offset_deg):
        self.drive_motor = TalonFX(drive_motor_id)
        self.steer_motor = TalonFX(steer_motor_id)
        self.abs_encoder = CANcoder(encoder_id)

        # Set neutral modes from constants
        self.drive_motor.setNeutralMode(ELEC.driveMotor_neutral)
        self.steer_motor.setNeutralMode(ELEC.steerMotor_neutral)

        # Physical mounting offset
        self.angle_offset = math.radians(angle_offset_deg)

        # Steering PID
        steer_cfg = TalonFXConfiguration()
        steer_cfg.slot0.k_p = 2.5
        steer_cfg.slot0.k_d = 0.1
        self.steer_motor.configurator.apply(steer_cfg)

        # Drive PID
        drive_cfg = TalonFXConfiguration()
        drive_cfg.slot0.k_p = 0.1
        self.drive_motor.configurator.apply(drive_cfg)

        # Sync steering to absolute encoder
        self._sync_to_absolute()

    def get_absolute_angle(self):
        """Returns the current angle in radians."""
        raw = self.abs_encoder.get_absolute_position().value  # 0–1 rotations
        angle = (raw * 2 * math.pi) - self.angle_offset
        return angle

    def _sync_to_absolute(self):
        """Sync steering motor to absolute encoder."""
        rad = self.get_absolute_angle()
        rotations = rad / (2 * math.pi) * MECH.swerve_module_steering_gearing_ratio
        self.steer_motor.set_position(rotations)

    def set(self, speed_mps, target_angle_rad):
        """Set speed and angle for this swerve module."""
        current = self.get_absolute_angle()
        delta = (target_angle_rad - current + math.pi) % (2 * math.pi) - math.pi

        # Flip wheel direction if needed
        if abs(delta) > math.pi / 2:
            speed_mps *= -1
            target_angle_rad += math.pi
            target_angle_rad %= 2 * math.pi

        # Steering motor control with gearing ratio
        steer_rotations = target_angle_rad / (2 * math.pi) * MECH.swerve_module_steering_gearing_ratio
        self.steer_motor.set_control(PositionVoltage(steer_rotations))

        # Drive motor control: speed in m/s -> rotations/sec using gearing ratio
        wheel_circ = math.pi * PHYS.wheel_diameter_meters
        motor_rps = (speed_mps / wheel_circ) * MECH.swerve_module_driving_gearing_ratio
        self.drive_motor.set_control(VelocityVoltage(motor_rps))


class SwerveDriveSubsystemClass(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        # --------------- CREATE MODULES USING CAN IDs ---------------
        self.front_right = SwerveModule(
            ELEC.RF_drive_CAN_ID,
            ELEC.RF_steer_CAN_ID,
            ELEC.RF_encoder_DIO,
            45
        )
        self.back_right = SwerveModule(
            ELEC.RB_drive_CAN_ID,
            ELEC.RB_steer_CAN_ID,
            ELEC.RB_encoder_DIO,
            0
        )
        self.back_left = SwerveModule(
            ELEC.LB_drive_CAN_ID,
            ELEC.LB_steer_CAN_ID,
            ELEC.LB_encoder_DIO,
            180
        )
        self.front_left = SwerveModule(
            ELEC.LF_drive_CAN_ID,
            ELEC.LF_steer_CAN_ID,
            ELEC.LF_encoder_DIO,
            135
        )

        # --------------- ROBOT GEOMETRY ---------------
        L = PHYS.wheelbase_meters
        W = PHYS.trackwidth_meters
        self.kinematics = SwerveDrive2Kinematics(
            Translation2d(+W/2, +L/2),  # Front Left
            Translation2d(+W/2, -L/2),  # Front Right
            Translation2d(-L/2, W/2), # Back Left 
            Translation2d(-L/2, -W/2) # Back Right 
        )

        # --------------- GYRO ---------------
        self.gyro = wpilib.ADIS16470_IMU()

    def drive(self, x_mps, y_mps, rot_rad_per_s, field_relative=True):
        """Drives the robot using x, y, rotation velocities."""
        if field_relative:
            chassis = wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(
                x_mps, y_mps, rot_rad_per_s,
                Rotation2d.fromDegrees(self.gyro.getAngle())
            )
        else:
            chassis = wpimath.kinematics.ChassisSpeeds(
                x_mps, y_mps, rot_rad_per_s
            )

        # Convert chassis speeds to individual module states
        states = self.kinematics.toSwerveModuleStates(chassis)
        SwerveDrive2Kinematics.desaturateWheelSpeeds(states, 4.5)  # max velocity

        # Apply module speeds and angles
        self.front_left.set(states[0].speed, states[0].angle.radians())
        self.front_right.set(states[1].speed, states[1].angle.radians())

