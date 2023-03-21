from typing import Tuple
from controller import Robot
from PID import PID
import math

ROBOT_SCALE = 1.1

WHEEL_RADIUS = 0.03*ROBOT_SCALE
INTERWHEEL_DISTANE = 0.0720026*ROBOT_SCALE


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
        return (-self.left_position.getValue()+self.start_left, -self.right_position.getValue()+self.start_right)


def rotational_distance_to_linear(rot_distance_rad: float):
    '''
    v = r*omega 
    '''
    return rot_distance_rad*WHEEL_RADIUS


def rotational_to_robot_rotational(rot_turn_distance: float):
    return rot_turn_distance*WHEEL_RADIUS/INTERWHEEL_DISTANE


def get_rotational_distance_delta(intial_values: Tuple[float, float], final_values: Tuple[float, float]):
    rotation_distance = [
        final_values[0] - intial_values[0],
        final_values[1] - intial_values[1]
    ]
    return (rotation_distance[0]+rotation_distance[1])/2


def get_rotational_rotation_delta(intial_values: Tuple[float, float], final_values: Tuple[float, float]):
    rotation_distance = [
        final_values[0] - intial_values[0],
        final_values[1] - intial_values[1]
    ]
    return (rotation_distance[0]-rotation_distance[1])/2


class LinearTraveller:
    def __init__(self, pid_controller: PID, motorcontroller: Motorcontrol):
        self.motorcontroller = motorcontroller
        self.initial_position = (0.0, 0.0)
        self.target_distance = 0.0
        self.pid_controller = pid_controller

    def initialize(self, target_distance: float):
        '''
        upon intialization it will use the current position and travel a linear distance of target_distance
        '''
        self.initial_position = self.motorcontroller.get_position_values()
        self.target_distance = target_distance
        self.pid_controller.set_set_point(0)

    def run(self):
        '''
        motocontroller.set_pose_speed() must be called after this call to take effect
        '''
        current_position = self.motorcontroller.get_position_values()
        rotational_distance = get_rotational_distance_delta(
            self.initial_position, current_position)
        distance = rotational_distance_to_linear(rotational_distance)
        print(distance)
        error = self.target_distance - distance
        signal = self.pid_controller(error)
        self.motorcontroller.linear_speed = signal


class Rotator:
    def __init__(self, pid_controller: PID, motorcontroller: Motorcontrol):
        self.motorcontroller = motorcontroller
        self.initial_position = (0.0, 0.0)
        self.target_angle = 0.0
        self.pid_controller = pid_controller

    def initialize(self, target_angle: float):
        '''
        upon intialization it will use the current position and travel a linear distance of target_angle
        '''
        self.initial_position = self.motorcontroller.get_position_values()
        self.target_angle = target_angle
        self.pid_controller.set_set_point(0)

    def run(self):
        '''
        motocontroller.set_pose_speed() must be called after this call to take effect
        '''
        current_position = self.motorcontroller.get_position_values()
        rotational_distance = get_rotational_rotation_delta(
            self.initial_position, current_position)
        angle = rotational_to_robot_rotational(rotational_distance)
        print(angle)
        error = self.target_angle - angle
        signal = self.pid_controller(error)
        self.motorcontroller.rotational_speed = signal
