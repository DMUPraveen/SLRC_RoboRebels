from typing import Tuple
from controller import Robot
import numpy as np


class Motorcontrol:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.maxvelocity = -3
        self.left_motor1 = self.robot.getMotor("Left_motor1")
        self.right_motor1 = self.robot.getMotor("Right_motor1")
        self.left_motor1.setPosition(float('inf'))
        self.right_motor1.setPosition(float('inf'))
        self.left_motor1.setVelocity(0)
        self.right_motor1.setVelocity(0)

        self.linear_speed = 0.0
        self.rotational_speed = 0.0

        right_position = self.right_motor1.getPositionSensor()
        assert(right_position is not None)
        self.right_position = right_position
        left_position = self.left_motor1.getPositionSensor()
        assert(left_position is not None)
        self.left_position = left_position
        sampling_time = int(robot.getBasicTimeStep())
        self.right_position.enable(sampling_time)
        self.left_position.enable(sampling_time)
        self.start_left = self.left_position.getValue()
        self.start_right = self.right_position.getValue()

    def setspeed(self, left_motor_v, right_motor_v):
        # left_motor_v=left_motor_v*self.maxvelocity
        # right_motor_v=right_motor_v*self.maxvelocity
        self.left_motor1.setVelocity(left_motor_v)
        self.right_motor1.setVelocity(right_motor_v)

    def simpleforward(self):
        self.left_motor1.setVelocity(self.maxvelocity)
        self.right_motor1.setVelocity(self.maxvelocity)

    def simpleturnleft(self):
        self.left_motor1.setVelocity(-self.maxvelocity)
        self.right_motor1.setVelocity(self.maxvelocity)

    def simplestop(self):
        self.left_motor1.setVelocity(0)
        self.right_motor1.setVelocity(0)

    def set_pose_speed(self):
        self.setspeed(self.linear_speed+self.rotational_speed,
                      self.linear_speed-self.rotational_speed)

    def get_position_values(self):
        '''
        returns the position sensor values of the motors they are decreasing for forward direction
        therefore it is negated the intial value is added so that the starting value will be zero
        '''
        return np.array((-self.left_position.getValue()+self.start_left, -self.right_position.getValue()+self.start_right))

    def get_pos_sensors(self):
        return self.left_position, self.right_position

    def pose_stop(self):
        self.linear_speed = 0
        self.rotational_speed = 0
