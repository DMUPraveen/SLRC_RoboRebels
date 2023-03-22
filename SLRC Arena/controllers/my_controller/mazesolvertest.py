from controller import Robot
from DistanceSensors import DistanceSensors
from Motors import Motorcontrol
from PID import PID
from Navigation import Alingment, LinearTraveller, Rotator
from Grid import Grid, GridNode, str_abs_dirs, NORTH, SOUTH, EAST, WEST
from GraphicEngine import GraphicEngine, BLUE
from MazeRunner import MazeRunner
from MazeSolver import MazeSolver
import math


def main():
    # print("Hello")
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
    # grid = Grid(7, 7)
    gfx = GraphicEngine(400, 400)
    mazeRunner = MazeRunner(
        motorcontrol, distancesensors, lineartraveller, rotator, 7)
    task_runner = mazeRunner.run_execution_stack()
    mazeRunner.add_task_aling()
    mazeRunner.add_task_build_wall()
    mazesolver = MazeSolver(mazeRunner)
    mazesolver.initialize()
    while robot.step(timestep) != -1:
        ############################# Draw Code ######################################
        gfx.clear()
        y, x = mazeRunner.grid_position
        gfx.draw_cell(BLUE, x, y)
        for row in mazeRunner.grid.grid:
            for node in row:
                gfx.draw_node(node)
        gfx.run()
        ##############################################################################

        finished = task_runner.__next__()
        if(finished):
            status = mazesolver.run_bfs()
            if(status):
                print("Search Complete")
        motorcontrol.set_pose_speed()
