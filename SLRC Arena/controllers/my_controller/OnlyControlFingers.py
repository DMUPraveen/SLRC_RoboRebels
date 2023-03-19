""" Only Controls Fingers"""

from ArmController import armcontroll
from controller import Robot, Supervisor
from PositionSensors import Positions
from SuperArm import Armstatemachine
from Motors import Motorcontrol
from Boxdetector import BoxDetector
from SuperStateMachineForCatchTheBox import SuperState


def main():
    robot=Robot()
    timestep = int(robot.getBasicTimeStep())
    # arm=armcontroll(robot)
    # car=Motorcontrol(robot)
    # pos=Positions(robot,arm)
    # superarm=Armstatemachine(robot,arm,pos,car)
    # boxdetect=BoxDetector(robot,car)
    # superduper=SuperState(robot,superarm,boxdetect)

    # finger_motor_right = robot.getMotor('right_finger_motor')
    # finger_motor_left = robot.getMotor('left_finger_motor')

    while robot.step(timestep) != -1:
        # finger_motor_right.setPosition(-1)
        # finger_motor_right.setVelocity(2)
        # finger_motor_left.setPosition(1)
        # finger_motor_left.setVelocity(2)
        pass