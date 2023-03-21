from controller import Robot
from DistanceSensors import DistanceSensors
from Motors import Motorcontrol


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    distancesensors = DistanceSensors(robot, timestep)
    while robot.step(timestep) != -1:
        distancesensors.debug_print()
        pass
