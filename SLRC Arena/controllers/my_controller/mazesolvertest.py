from controller import Robot
from DistanceSensors import DistanceSensors
from Motors import Motorcontrol
from PID import PID
from Navigation import Alingment, LinearTraveller, Rotator
import math


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    distancesensors = DistanceSensors(robot, timestep)
    motorcontrol = Motorcontrol(robot)
    alignment = Alingment(motorcontrol, distancesensors)
    linear_traveller_pid = PID(50, 0, 0)
    lineartravelleter = LinearTraveller(linear_traveller_pid, motorcontrol)
    lineartravelleter.initialize(0.36)
    rotator_pid = PID(10, 0, 0)
    rotator = Rotator(rotator_pid, motorcontrol)
    rotator.initialize(-math.pi)

    while robot.step(timestep) != -1:
        # lineartravelleter.run()
        print(alignment.align_to_back_wall())
        motorcontrol.set_pose_speed()
