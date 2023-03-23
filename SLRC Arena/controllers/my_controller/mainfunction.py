"""my_controller controller."""
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
from Grabber import GrabBox


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
from ClassForPuttingBackTheBox import PutTHEDAMNBOX
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
    # alignment = Alingment(motorcontrol, distancesensors)
    # linear_traveller_pid = PID(50, 0, 0)
    # lineartraveller = LinearTraveller(linear_traveller_pid, motorcontrol)
    # lineartraveller.initialize(0.36)
    # rotator_pid = PID(10, 0, 0)
    # rotator = Rotator(rotator_pid, motorcontrol)
    # rotator.initialize(-math.pi)
    # # grid = Grid(7, 7)
    # gfx = GraphicEngine(400, 400)
    # mazeRunner = MazeRunner(
    #     motorcontrol, distancesensors, lineartraveller, rotator, 7)
    # task_runner = mazeRunner.run_execution_stack()
    # mazeRunner.add_task_aling()
    # mazeRunner.add_task_build_wall_smart()
    # # mazeRunner.add_back_centering_task()
    # mazeRunner.add_total_centering_taks()
    # mazesolver = MazeSolver(mazeRunner)
    # mazesolver.initialize()
    # mazegoto = Mazegoto(mazesolver)

######################## Arm Import #######################
    arm = armcontroll(robot)
    pos = Positions(robot, arm)
    superarm = Armstatemachine(robot, arm, pos, motorcontrol)
    boxdetect = BoxDetector(robot, motorcontrol)
    cam = Camera(robot, motorcontrol)
    superduper = SuperState(robot, superarm, boxdetect, cam)
    putboxdown=PutTHEDAMNBOX(robot,arm,pos)
    Hano = Hanoi(robot, arm, pos, boxdetect, motorcontrol, cam,putboxdown)
    grab=GrabBox(robot)
###########################################################
    # main_task = main_control_code(
    #     mazesolver, mazegoto, motorcontrol, superduper, Hano)
    new=0
    n=0
    while robot.step(timestep) != -1:
        # if new==0 and superduper.SuperStateMachine():
        #     new=1
        # if new==1:
        #     n+=1
        # if n<100:
        # Hano.BuildHanoi(1)
        # motorcontrol.set_pose_speed()
        # print(cam.isAligned())
        # Hano.BuildHanoi(1)
        grab.grab()
        
        pass

# if __name__=="__main__":
#     main()


    

