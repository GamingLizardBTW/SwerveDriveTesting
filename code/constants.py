"""
This file defines constants related to your robot.  These constants include:

 * Physical constants (exterior dimensions, wheel base)

 * Mechanical constants (gear reduction ratios)

 * Electrical constants (current limits, CAN bus IDs, roboRIO slot numbers)

 * Operation constants (desired max velocity, max turning speed)

 * Software constants (USB ID for driver joystick)
"""

from collections import namedtuple

# Physical constants, e.g. wheel circumference, physical dimensions
phys_data = {
}
PHYS = namedtuple("Data", phys_data.keys())(**phys_data)

# Mechanical constants, e.g. gearing ratios, whether motors are inverted
mech_data = {
}
MECH = namedtuple("Data", mech_data.keys())(**mech_data)

# Electrical constants, e.g. current limits, CAN bus IDs, RoboRIO port numbers
elec_data = {
  ## First motor
  "first_motor_CAN_ID": 3,
  "first_motor_forward":0.1,
  "first_motor_reverse":-0.1,
  "first_motor_stop":0.0,

  ## Second motor
  "second_motor_CAN_ID": 2,
  "second_motor_forward":1.0,
  "second_motor_reverse":-1.0,
  "second_motor_stop":0.0,

  ## Limit Switch
  "limit_switch_port":0,

}
ELEC = namedtuple("Data", elec_data.keys())(**elec_data)

# Operation constants, e.g. preferred brake mode, which joystick to use
op_data = {
    "joystick_port": 0,
}
OP = namedtuple("Data", op_data.keys())(**op_data)

# Software constants, e.g. PID values, absolute encoder zero points
sw_data = {
# SecondMotor PID Constats
    "Second_ks": 3,
    "Second_kv": 0.12,
    "Second_ka": 0,
    "Second_kp": 45,
    "Second_ki": 0.01,
    "Second_kd": 0.01,

    "Second_Cruise_Velocity": 5,    # rotations/second
    "Second_Acceleration": 2,       # rotations/s^2
    "Second_Jerk": 500,              # rotations/s^3

    #"Second_Gear_Ratio": 1.0,        # update if needed

    "Second_Tolerance": 0.15,
    "Second_Speed_Tolerance": 0.2,

    "FirstMotorSetpoint": 0.01,
}
SW = namedtuple("Data", sw_data.keys())(**sw_data)
