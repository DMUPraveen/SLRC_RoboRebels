from controller import Robot
from DistanceSensors import DistanceSensors
from Motors import Motorcontrol
from Navigation import Navigation


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    distancesensors = DistanceSensors(robot, timestep)
    motorcontrol = Motorcontrol(robot)
    navigation = Navigation(motorcontrol, distancesensors)
    while robot.step(timestep) != -1:
        left_wall_error = distancesensors.left_wall_align_error()
        right_wall_error = distancesensors.right_wall_align_error()
        print(f"{left_wall_error=:.2f} and {right_wall_error=:.2f}")
        left_wall_distance = distancesensors.average_left_wall_distance()
        right_wall_distance = distancesensors.average_right_wall_distance()
        print(f"{left_wall_distance=:.2f} and {right_wall_distance=:.2f}")
        left_wall_present = distancesensors.left_wall_present()
        right_wall_present = distancesensors.right_wall_present()
        print(f"{left_wall_present=:.2f} and {right_wall_present=:.2f}")
        navigation.align_to_right_wall()
        motorcontrol.set_pose_speed()
