from controller import Robot
from DistanceSensors import DistanceSensors
from Motors import Motorcontrol
from PID import PID
from Navigation import Alingment, LinearTraveller, Rotator
from Grid import Grid, GridNode, str_abs_dirs
from GraphicEngine import GraphicEngine, BLUE
from MazeSolver import MazeRunner
import math


def main():
    print("Hello")
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    distancesensors = DistanceSensors(robot, timestep)
    motorcontrol = Motorcontrol(robot)
    alignment = Alingment(motorcontrol, distancesensors)
    linear_traveller_pid = PID(50, 0, 0)
    lineartraveller = LinearTraveller(linear_traveller_pid, motorcontrol)
    lineartraveller.initialize(0.36)
    rotator_pid = PID(10, 0, 0)
    rotator = Rotator(rotator_pid, motorcontrol)
    rotator.initialize(-math.pi)
    grid = Grid(7, 7)
    gfx = GraphicEngine(400, 400)
    mazesolver = MazeRunner(
        motorcontrol, distancesensors, lineartraveller, rotator, 7)

    run_code = mazesolver.test_run()
    while robot.step(timestep) != -1:
        # lineartraveller.run()
        gfx.clear()
        y, x = mazesolver.grid_position
        gfx.draw_cell(BLUE, x, y)
        print(str_abs_dirs(mazesolver.orientation))
        for row in mazesolver.grid.grid:
            for node in row:
                gfx.draw_node(node)
        gfx.run()
        run_code.__next__()
        motorcontrol.set_pose_speed()
