from controller import Robot
import numpy as np
from ArmController import armcontroll
##Testing Arm

def run_robot2(robot):
    arm=armcontroll(robot)
    arm.putinback(-11,0,0,0,0)