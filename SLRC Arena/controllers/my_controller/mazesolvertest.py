from controller import Robot
from DistanceSensors import DistanceSensors
from Motors import Motorcontrol
from PID import PID
from Navigation import Alingment, LinearTraveller, Rotator
from Grid import Grid, GridNode, str_abs_dirs, NORTH, SOUTH, EAST, WEST
from GraphicEngine import GraphicEngine, BLUE, RED
from MazeRunner import MazeRunner
from MazeSolver import MazeSolver
from Mazegoto import Mazegoto
from mainControlCode import main_control_code
import math


######################## Arm Import #######################
from ArmController import armcontroll
from controller import Robot, Supervisor
from PositionSensors import Positions
from SuperArm import Armstatemachine
from Motors import Motorcontrol
from Boxdetector import BoxDetector
from SuperStateMachineForCatchTheBox import SuperState
from CameraClass import Camera
from PlacingOnTop import Hanoi
###########################################################

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

STACK_COLORS = [YELLOW, CYAN, MAGENTA]


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
    mazeRunner.add_task_build_wall_smart()
    # mazeRunner.add_back_centering_task()
    mazeRunner.add_total_centering_taks()
    mazesolver = MazeSolver(mazeRunner)
    mazesolver.initialize()
    mazegoto = Mazegoto(mazesolver)

######################## Arm Import #######################
    arm = armcontroll(robot)
    pos = Positions(robot, arm)
    superarm = Armstatemachine(robot, arm, pos, motorcontrol)
    boxdetect = BoxDetector(robot, motorcontrol)
    cam = Camera(robot, motorcontrol)
    superduper = SuperState(robot, superarm, boxdetect, cam)
    Hano = Hanoi(robot, arm, pos, boxdetect, motorcontrol, cam)
###########################################################
    main_task = main_control_code(
        mazesolver, mazegoto, motorcontrol, superduper, Hano)
    while robot.step(timestep) != -1:
        ############################# Draw Code ######################################
        gfx.clear()
        y, x = mazeRunner.grid_position
        gfx.draw_cell(BLUE, x, y)
        for corner in mazesolver.corners:
            y, x = corner
            gfx.draw_cell(RED, x, y)
        for index, pos in enumerate(mazegoto.stacks):
            y, x = pos
            gfx.draw_cell(STACK_COLORS[index], x, y)
        for row in mazeRunner.grid.grid:
            for node in row:
                gfx.draw_node(node)
        gfx.run()
        ##############################################################################
        finished = task_runner.__next__()
        if(finished):
            main_task.__next__()

        motorcontrol.set_pose_speed()
