import numpy as np

def turn90encoder():
    r_wheel = 4.95/2
    r_robot = 8.5
    c_robot = r_robot*(np.pi/2)
    c_wheel = r_wheel*np.pi*2
    encorder_pulse_per_rev = 550
    rev_wheel = c_robot/c_wheel
    encoder_count = rev_wheel*encorder_pulse_per_rev

    return encoder_count

def encoder_count_poddakMoveForward():
    c_wheel = 8.5*np.pi/2
    rev_wheel = 1/c_wheel
    enc_count = rev_wheel*550

    return enc_count

print(turn90encoder())
print(encoder_count_poddakMoveForward())
