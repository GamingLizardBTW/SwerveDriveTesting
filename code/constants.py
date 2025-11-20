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
    "First_ks": 0.2,     # Static friction
    "First_kv": 0.12,    # Velocity feedforward
    "First_ka": 0.0,     # Acceleration feedforward raise if system needs to be faster

    "First_kp": 3.0,     # Too high and will cause oscillation, too low will make it not reach desired place
    "First_ki": 0.5,     # Helps fix small errors over time 
    "First_kd": 0.1,     # Stabalizing, fixes over shoot

    # Motion Magic
    "First_Cruise_Velocity": 40,   # rotations/sec   Max Speed
    "First_Acceleration": 80,      # rotations/sec^2 How fast it can accelerate
    "First_Jerk": 0,               # optional        First push to start acceleration

    "First_Gear_Ratio": 1.0,       #change if motor has gearing

    # Setpoint for testing
    "FirstMotorSetpoint": 5.0,     #rotations
}
SW = namedtuple("Data", sw_data.keys())(**sw_data)
