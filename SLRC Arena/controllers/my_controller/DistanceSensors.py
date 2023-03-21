from controller import Robot
from controller import DistanceSensor
from typing import List


FRONT = "front"

FRONT_LEFT = "front_left"
FRONT_RIGHT = "front_right"

LEFT_FRONT = "left_front"
RIGHT_FRONT = "right_front"

LEFT_BACK = "left_back"
RIGHT_BACK = "right_back"

BACK_LEFT = "back_left"
BACK_RIGHT = "back_right"


class DistanceSensors:
    def __init__(self, robot: Robot, sampling_period):
        self.sampling_period = sampling_period

        self.front: DistanceSensor = robot.getDevice(FRONT)  # type: ignore

        self.front_left: DistanceSensor = robot.getDevice(
            FRONT_LEFT)  # type: ignore
        self.front_right: DistanceSensor = robot.getDevice(
            FRONT_RIGHT)  # type: ignore

        self.left_front: DistanceSensor = robot.getDevice(
            LEFT_FRONT)  # type: ignore
        self.right_front: DistanceSensor = robot.getDevice(
            RIGHT_FRONT)  # type: ignore

        self.left_back: DistanceSensor = robot.getDevice(
            LEFT_BACK)  # type: ignore
        self.right_back: DistanceSensor = robot.getDevice(
            RIGHT_BACK)  # type: ignore

        self.back_left: DistanceSensor = robot.getDevice(
            BACK_LEFT)  # type: ignore
        self.back_right: DistanceSensor = robot.getDevice(
            BACK_RIGHT)  # type: ignore

        self.all_sensors: List[DistanceSensor] = [  # type: ignore
            self.left_back,
            self.left_front,
            self.front_left,
            self.front,
            self.front_right,
            self.right_front,
            self.right_back,
            self.back_left,
            self.back_right
        ]
        for sensor in self.all_sensors:
            sensor.enable(self.sampling_period)  # type: ignore

        self.max_value: float = self.front.getMaxValue()  # type: ignore
        for sensor in self.all_sensors:
            assert(sensor.getMaxValue() == self.max_value)  # type: ignore

    def debug_print(self):
        print(
            ",".join(f"{sensor.getValue():.2f}" for sensor in self.all_sensors))

    def left_wall_align_error(self):
        return (self.left_front.getValue()-self.left_back.getValue())/self.max_value

    def right_wall_align_error(self):
        return (self.right_back.getValue() - self.right_front.getValue())/self.max_value

    def back_wall_align_error(self):
        return (self.back_left.getValue() - self.back_right.getValue())/self.max_value

    def average_left_wall_distance(self):
        return (self.left_front.getValue()+self.left_back.getValue())/2/self.max_value

    def average_right_wall_distance(self):
        return (self.right_front.getValue()+self.right_back.getValue())/2/self.max_value

    def average_back_wall_distance(self):
        return (self.back_left.getValue()+self.back_right.getValue())/2/self.max_value

    def left_wall_present(self):
        return self.average_left_wall_distance() < 1

    def right_wall_present(self):
        return self.average_right_wall_distance() < 1

    def back_wall_present(self):
        return self.average_back_wall_distance() < 1
