"""
This file defines constants related to your robot. These constants include:

 * Physical constants (exterior dimensions, wheelbase)
 * Mechanical constants (gear reduction ratios)
 * Electrical constants (current limits, CAN bus IDs)
 * Operation constants (desired max velocity, controller port)
 * Software constants (swerve settings, PID, motion magic, etc.)
"""

from collections import namedtuple
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDriveKinematics



phys_data = {
    # Replace these with robot dimensions in meters
    "wheelbase_meters": 0.5,     #length of robot from front to back 
    "trackwidth_meters": 0.5,    #lenght of robot from left to right
}
PHYS = namedtuple("PHYS", phys_data.keys())(**phys_data)



mech_data = {
    #Add gear ratios here when needed later
}
MECH = namedtuple("MECH", mech_data.keys())(**mech_data)


elec_data = {
    #First motor
    "first_motor_CAN_ID": 3,
    "first_motor_forward": 0.5,
    "first_motor_reverse": -0.5,
    "first_motor_stop": 0.0,

    #Second motor
    "second_motor_CAN_ID": 2,
    "second_motor_forward": 1.0,
    "second_motor_reverse": -1.0,
    "second_motor_stop": 0.0,

    "limit_switch_port": 0,

    #Swerve module motors
    "front_left_drive_id": 1,
    "front_left_turn_id": 2,

    "front_right_drive_id": 3,
    "front_right_turn_id": 4,

    "rear_left_drive_id": 5,
    "rear_left_turn_id": 6,

    "rear_right_drive_id": 7,
    "rear_right_turn_id": 8,
}
ELEC = namedtuple("ELEC", elec_data.keys())(**elec_data)



op_data = {
    "joystick_port": 0,
}
OP = namedtuple("OP", op_data.keys())(**op_data)



sw_data = {
    #First motor PID
    "First_ks": 0.2,
    "First_kv": 0.12,
    "First_ka": 0.0,

    "First_kp": 3.0,
    "First_ki": 0.5,
    "First_kd": 0.1,

    "First_Cruise_Velocity": 40,
    "First_Acceleration": 80,
    "First_Jerk": 0,

    "First_Gear_Ratio": 1.0,
    "FirstMotorSetpoint": 10.0,

    # Swerve speed limits
    "swerve_max_speed_mps": 3.0,           # Robot max linear speed
    "swerve_max_angular_speed_rps": 3.0,   # Robot max turning speed
}
SW = namedtuple("SW", sw_data.keys())(**sw_data)


# Module physical locations relative to robot center
front_left_location = Translation2d(PHYS.wheelbase_meters / 2,  PHYS.trackwidth_meters / 2)
front_right_location = Translation2d(PHYS.wheelbase_meters / 2, -PHYS.trackwidth_meters / 2)
rear_left_location = Translation2d(-PHYS.wheelbase_meters / 2,  PHYS.trackwidth_meters / 2)
rear_right_location = Translation2d(-PHYS.wheelbase_meters / 2, -PHYS.trackwidth_meters / 2)

# Main shared kinematics object
SWERVE_KINEMATICS = SwerveDriveKinematics(
    front_left_location,
    front_right_location,
    rear_left_location,
    rear_right_location
)
