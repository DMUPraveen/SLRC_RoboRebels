
from Motors import Motorcontrol
from DistanceSensors import DistanceSensors
from PID import PID

import math
import numpy as np
import numpy.typing as npt

ROBOT_SCALE = 1.1
ROBOT_LENGTH = 0.2*ROBOT_SCALE
WHEEL_RADIUS = 0.03*ROBOT_SCALE
INTERWHEEL_DISTANE = 0.0720026*ROBOT_SCALE
BACK_SENSOR_OFFSET = ROBOT_SCALE*0.07
cell_size_in_meters = 0.36
WHEEL_TRANSLATION = 0.0299874*ROBOT_SCALE
CENTER_DISTANCE = 0.34/2 - BACK_SENSOR_OFFSET - WHEEL_TRANSLATION


def rotational_distance_to_linear(rot_distance_rad: float):
    '''
    v = r*omega 
    '''
    return rot_distance_rad*WHEEL_RADIUS


def rotational_to_robot_rotational(rot_turn_distance: float):
    return rot_turn_distance*WHEEL_RADIUS/INTERWHEEL_DISTANE


def get_rotational_distance_delta(intial_values, final_values):

    # rotation_distance = [
    #     final_values[0] - intial_values[0],
    #     final_values[1] - intial_values[1]
    # ]
    rotation_distance = final_values - intial_values
    return (rotation_distance[0]+rotation_distance[1])/2


def get_rotational_rotation_delta(intial_values, final_values):
    # rotation_distance = [
    #     final_values[0] - intial_values[0],
    #     final_values[1] - intial_values[1]
    # ]
    rotation_distance = final_values - intial_values
    return (rotation_distance[0]-rotation_distance[1])/2


def from_distance_sensor_to_meters(distance: float):
    return distance/10*2


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
        # print(distance)
        error = self.target_distance - distance
        signal = self.pid_controller(error)
        self.motorcontroller.linear_speed = signal
        return abs(error)


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
        # print(angle)
        error = self.target_angle - angle
        signal = self.pid_controller(error)
        self.motorcontroller.rotational_speed = signal
        return abs(error)


def delta_to_rotational_matrix(delta_radian):
    return np.array(
        [
            [np.cos(delta_radian), -np.sin(delta_radian)],
            [np.sin(delta_radian), np.cos(delta_radian)]
        ]
    )


class PoseEstimator:
    def __init__(self, motorcontroller: Motorcontrol):
        self.position = np.zeros(2, dtype="float64")
        self.rotation_vector = np.array([1, 0], dtype='float64')
        self.previous_values = np.zeros(2)
        self.motorcontroller = motorcontroller

    def estimate(self):
        current_values = self.motorcontroller.get_position_values()

        linear_delta_rotational = get_rotational_distance_delta(
            self.previous_values, current_values)
        linear_delta = rotational_distance_to_linear(linear_delta_rotational)

        rotation_delta_rotational = get_rotational_rotation_delta(
            self.previous_values, current_values)
        rotational_delta = rotational_to_robot_rotational(
            rotation_delta_rotational)

        new_rotational_vector = delta_to_rotational_matrix(
            rotational_delta) @ self.rotation_vector
        new_position = self.position + linear_delta * \
            (new_rotational_vector+self.rotation_vector)/2

        self.rotation_vector = new_rotational_vector
        self.position = new_position

        self.previous_values = current_values

    def get_pose_angle(self):
        return np.arctan2(self.rotation_vector[0], self.rotation_vector[1])

    def get_position(self):
        return self.position.copy()

    def __str__(self):
        return f"{self.position[0]:.3f},{self.position[1]:.3f} @ {self.get_pose_angle():.3f}"

    def __repr__(self) -> str:
        return self.__str__()


class Alingment:
    def __init__(self, motorController: Motorcontrol, distanceSensors: DistanceSensors):
        self.motorController = motorController
        self.distanceSensors = distanceSensors
        self.left_aling_pid = PID(30, 0, 0)
        self.right_aling_pid = self.left_aling_pid.create_copy()
        self.back_align_pid = self.right_aling_pid.create_copy()
        self.centering_pid = self.left_aling_pid.create_copy()
        self.left_aling_pid.set_set_point(0)
        self.right_aling_pid.set_set_point(0)
        self.back_align_pid.set_set_point(0)
        self.centering_pid.set_set_point(0)

    def align_to_left_wall(self):
        '''
        aligns to left wall does not check whether both sensor are engaged 
        returns the error
        this does not the motor velocity but the pose, motorsController.pose_control()
        must be called in order to activated this
        '''
        measurement = self.distanceSensors.left_wall_align_error()
        control_signal = self.left_aling_pid(measurement)
        self.motorController.rotational_speed = -control_signal
        return abs(measurement)

    def align_to_right_wall(self):
        '''
        aligns to right wall does not check whether both sensor are engaged 
        returns the error
        this does not the motor velocity but the pose, motorsController.pose_control()
        must be called in order to activated this
        '''
        measurement = self.distanceSensors.right_wall_align_error()
        control_signal = self.right_aling_pid(measurement)
        self.motorController.rotational_speed = -control_signal
        return abs(measurement)

    def align_to_back_wall(self):
        '''
        aligns to right wall does not check whether both sensor are engaged 
        returns the error
        this does not the motor velocity but the pose, motorsController.pose_control()
        must be called in order to activated this
        '''
        measurement = self.distanceSensors.back_wall_align_error()
        control_signal = self.right_aling_pid(measurement)
        self.motorController.rotational_speed = -control_signal
        return abs(measurement)

    def center_back_error(self):
        return from_distance_sensor_to_meters(self.distanceSensors.average_back_wall_distance()) - CENTER_DISTANCE

    def center_using_back_sensor(self):
        print("Running center using back sensor")
        measurement = self.center_back_error()
        print(measurement, self.distanceSensors.average_back_wall_distance(),
              ROBOT_LENGTH, cell_size_in_meters, CENTER_DISTANCE, self.distanceSensors.average_left_wall_distance())
        control_signal = self.back_align_pid(measurement)
        self.motorController.linear_speed = -control_signal
        return abs(measurement)
