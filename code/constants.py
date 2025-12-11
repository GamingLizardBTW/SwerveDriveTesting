"""
This file defines constants related to your robot. These constants include:

 * Physical constants (robot dimensions, wheelbase)
 * Mechanical constants (gear ratios, motor inversion)
 * Electrical constants (CAN IDs, current limits)
 * Operation constants (joystick ports)
 * Software constants (PID values, swerve max speeds)
"""

from collections import namedtuple
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive2Kinematics, SwerveModuleState

# -----------------------------
# Physical constants
# -----------------------------
phys_data = {
    "wheelbase_meters": 0.5,   # front ↔ back distance
    "trackwidth_meters": 0.5,  # left ↔ right distance
    "wheel_diameter_meters": 0.1016,  # 4-inch wheels
}

PHYS = namedtuple("Data", phys_data.keys())(**phys_data)

# -----------------------------
# Mechanical constants
# -----------------------------
mech_data = {
    "first_motor_inverted": False,
    "second_motor_inverted": False,
    # Add more gearing or inversion constants here
}

MECH = namedtuple("Data", mech_data.keys())(**mech_data)

# -----------------------------
# Electrical constants
# -----------------------------
elec_data = {
    "first_motor_CAN_ID": 3,
    "first_motor_forward": 0.5,
    "first_motor_reverse": -0.5,
    "first_motor_stop": 0.0,

    "second_motor_CAN_ID": 2,
    "second_motor_forward": 1.0,
    "second_motor_reverse": -1.0,
    "second_motor_stop": 0.0,

    "limit_switch_port": 0,
}

ELEC = namedtuple("Data", elec_data.keys())(**elec_data)

# -----------------------------
# Operation constants
# -----------------------------
op_data = {
    "joystick_port": 0,
}

OP = namedtuple("Data", op_data.keys())(**op_data)

# -----------------------------
# Software constants (PID, feedforward, swerve speeds)
# -----------------------------
sw_data = {
    # First motor PID
    "First_ks": 0.2,
    "First_kv": 0.12,
    "First_ka": 0.0,
    "First_kp": 3.0,
    "First_ki": 0.5,
    "First_kd": 0.1,

    # Motion Magic
    "First_Cruise_Velocity": 40,
    "First_Acceleration": 80,
    "First_Jerk": 0,
    "First_Gear_Ratio": 1.0,
    "FirstMotorSetpoint": 10.0,

    # Swerve-specific speeds
    "swerve_max_speed_mps": 3.0,          # max linear speed (meters/sec)
    "swerve_max_angular_speed_rps": 4.0,  # max rotational speed (rad/sec)
}

SW = namedtuple("Data", sw_data.keys())(**sw_data)

# -----------------------------
# Swerve module positions (front-left & front-right only)
# -----------------------------
front_left_location  = Translation2d(float(PHYS.wheelbase_meters) / 2,  float(PHYS.trackwidth_meters) / 2)
front_right_location = Translation2d(float(PHYS.wheelbase_meters) / 2, -float(PHYS.trackwidth_meters) / 2)

# -----------------------------
# Swerve drive kinematics object
# -----------------------------
SWERVE_KINEMATICS = SwerveDrive2Kinematics(front_left_location, front_right_location)
