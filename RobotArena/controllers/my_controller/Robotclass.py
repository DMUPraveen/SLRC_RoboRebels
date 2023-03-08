from controller import Robot
import numpy as np
from ArmController import armcontroll
##Testing Arm

def takeup2(robot,waist_val,shoulder_val,elbow_val,wrist_val,pitch_val):
        waist_motor = robot.getDevice('waist_motor')
        shoulder_motor = robot.getDevice('shoulder_motor')
        elbow_motor = robot.getDevice('elbow_motor')
        wrist_motor = robot.getDevice('wrist_motor')
        pitch_motor = robot.getDevice('pitch_motor')
        shoulder_motor.setPosition(shoulder_val)
        pitch_motor.setPosition(pitch_val)
        elbow_motor.setPosition(elbow_val)
    