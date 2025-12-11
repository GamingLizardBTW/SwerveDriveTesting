"""
This file defines constants related to your robot. These constants include:

 * Physical constants (exterior dimensions, wheelbase)
 * Mechanical constants (gear reduction ratios)
 * Electrical constants (current limits, CAN bus IDs, roboRIO slot numbers)
 * Operation constants (desired max velocity, max turning speed)
 * Software constants (USB ID for driver joystick, PID values)
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
    # Add additional gearing or inversion constants here
}

MECH = namedtuple("Data", mech_data.keys())(**mech_data)

# -----------------------------
# Electrical constants
# -----------------------------
elec_data = {
    ## First motor
    "first_motor_CAN_ID": 3,
    "first_motor_forward": 0.5,
    "first_motor_reverse": -0.5,
    "first_motor_stop": 0.0,

    ## Second motor
    "second_motor_CAN_ID": 2,
    "second_motor_forward": 1.0,
    "second_motor_reverse": -1.0,
    "second_motor_stop": 0.0,

    ## Limit Switch
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
# Software constants (PID, feedforward, setpoints)
# -----------------------------
sw_data = {
    # First motor PID
    "First_ks": 0.2,
    "First_kv": 0.12,
    "First_ka": 0.0,
    "First_kp": 3.0,
    "First_ki": 0.5,
    "First_kd": 0.1,

    # Motion Magic (optional)
    "First_Cruise_Velocity": 40,
    "First_Acceleration": 80,
    "First_Jerk": 0,
    "First_Gear_Ratio": 1.0,
    "FirstMotorSetpoint": 10.0,

    # Swerve-specific max speeds
    "swerve_max_speed_mps": 3.0,       # max linear speed (m/s)
    "swerve_max_angular_speed_rps": 4.0,  # max rotation speed (rad/s)
}

SW = namedtuple("Data", sw_data.keys())(**sw_data)

# -----------------------------
# Swerve module positions (Translation2d)
# -----------------------------
front_left_location  = Translation2d(PHYS.wheelbase_meters / 2,  PHYS.trackwidth_meters / 2)
front_right_location = Translation2d(PHYS.wheelbase_meters / 2, -PHYS.trackwidth_meters / 2)
rear_left_location   = Translation2d(-PHYS.wheelbase_meters / 2,  PHYS.trackwidth_meters / 2)
rear_right_location  = Translation2d(-PHYS.wheelbase_meters / 2, -PHYS.trackwidth_meters / 2)

# -----------------------------
# Swerve drive kinematics object
# -----------------------------
SWERVE_KINEMATICS = SwerveDrive2Kinematics(
    front_left_location,
    front_right_location,
    rear_left_location,
    rear_right_location
)