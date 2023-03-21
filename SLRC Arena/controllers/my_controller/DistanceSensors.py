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

        self.all_sensors: List[DistanceSensor] = [  # type: ignore
            self.left_back,
            self.left_front,
            self.front_left,
            self.front,
            self.front_right,
            self.right_front,
            self.right_back
        ]
        for sensor in self.all_sensors:
            sensor.enable(self.sampling_period)  # type: ignore

    def debug_print(self):
        print(
            ",".join(f"{sensor.getValue():.2f}" for sensor in self.all_sensors))

    def left_wall_align_error(self):
        pass
