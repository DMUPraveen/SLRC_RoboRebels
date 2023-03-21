
from Motors import Motorcontrol
from DistanceSensors import DistanceSensors


class MazeSolver:
    def __init__(self, motorController: Motorcontrol, distanceSensors: DistanceSensors):
        self.motorController = motorController
        self.distanceSensors = distanceSensors
