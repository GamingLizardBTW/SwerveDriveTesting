import math
import wpilib
import wpimath
from wpilib import SmartDashboard
from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import SwerveDrive2Kinematics, SwerveModuleState
from phoenix6.hardware import TalonFX, CANcoder
from phoenix6.controls import PositionVoltage, VelocityVoltage
from phoenix6.configs import TalonFXConfiguration



class SwerveModule:
    def __init__(self, drive_motor_id, steer_motor_id, encoder_id, angle_offset_deg):
        self.drive_motor = TalonFX(drive_motor_id)
        self.steer_motor = TalonFX(steer_motor_id)
        self.abs_encoder = CANcoder(encoder_id)

        # Store physical mounting offset
        self.angle_offset = math.radians(angle_offset_deg)

        # Basic steering PID
        steer_cfg = TalonFXConfiguration()
        steer_cfg.slot0.k_p = 2.5
        steer_cfg.slot0.k_d = 0.1
        self.steer_motor.configurator.apply(steer_cfg)

        # Basic drive PID
        drive_cfg = TalonFXConfiguration()
        drive_cfg.slot0.k_p = 0.1
        self.drive_motor.configurator.apply(drive_cfg)

        # Sync steering to absolute encoder at boot
        self._sync_to_absolute()

    # Read absolute angle
    def get_absolute_angle(self):
        raw = self.abs_encoder.get_absolute_position().value  # 0–1 rotations
        angle = (raw * 2 * math.pi) - self.angle_offset
        return angle

    # Match steer motor to absolute encoder
    def _sync_to_absolute(self):
        rad = self.get_absolute_angle()
        rotations = rad / (2 * math.pi)
        self.steer_motor.set_position(rotations)

    # Set speed + angle of module
    def set(self, speed_mps, target_angle_rad):
        current = self.get_absolute_angle()
        delta = (target_angle_rad - current + math.pi) % (2 * math.pi) - math.pi

        # Flip wheel direction if needed
        if abs(delta) > math.pi / 2:
            speed_mps *= -1
            target_angle_rad += math.pi
            target_angle_rad %= 2 * math.pi

        # Set steering motor
        steer_rotations = target_angle_rad / (2 * math.pi)
        self.steer_motor.set_control(PositionVoltage(steer_rotations))

        # Convert drive m/s -> rotations/sec
        WHEEL_DIAMETER = 0.1016  # 4 inch wheel
        wheel_circ = math.pi * WHEEL_DIAMETER
        rps = speed_mps / wheel_circ

        self.drive_motor.set_control(VelocityVoltage(rps))


class SwerveDriveSubsystemClass(wpilib.SubsystemBase):
    def __init__(self):
        super().__init__()

        # --------------- CREATE MODULES ---------------
        self.front_left  = SwerveModule(1, 2, 11, 135)
        self.front_right = SwerveModule(3, 4, 12, 45)
        self.back_left   = SwerveModule(5, 6, 13, 225)
        self.back_right  = SwerveModule(7, 8, 14, 315)

        # --------------- ROBOT GEOMETRY ---------------
        L = 0.5
        W = 0.5
        self.kinematics = SwerveDrive2Kinematics(
            Translation2d(+W/2, +L/2),
            Translation2d(+W/2, -L/2),
            Translation2d(-W/2, +L/2),
            Translation2d(-W/2, -L/2),
        )

        # --------------- GYRO ---------------
        self.gyro = wpilib.ADIS16470_IMU()

    # DRIVE FUNCTION
    def drive(self, x_mps, y_mps, rot_rad_per_s, field_relative=True):
        if field_relative:
            chassis = wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(
                x_mps, y_mps, rot_rad_per_s,
                Rotation2d.fromDegrees(self.gyro.getAngle())
            )
        else:
            chassis = wpimath.kinematics.ChassisSpeeds(
                x_mps, y_mps, rot_rad_per_s
            )

        states = self.kinematics.toSwerveModuleStates(chassis)
        SwerveDrive2Kinematics.desaturateWheelSpeeds(states, 4.5)

        # Apply to modules
        self.front_left.set(states[0].speed, states[0].angle.radians())
        self.front_right.set(states[1].speed, states[1].angle.radians())
        self.back_left.set(states[2].speed, states[2].angle.radians())
        self.back_right.set(states[3].speed, states[3].angle.radians())
