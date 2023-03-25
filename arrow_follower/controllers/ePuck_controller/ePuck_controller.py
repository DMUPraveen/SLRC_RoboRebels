"""ePuck_controller controller."""

import sys

sys.path.insert(0,'C:\\Users\\msi\\Desktop\\SLRC_RoboRebels\\deploy_scripts')

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import main
from RobotManagerScript import RobotManager
from D_GAScript import D_GA
import numpy as np
import cv2

robot = RobotManager()
timestep = robot.timeStep

gameAgent = D_GA(robot)

while robot.step(timestep) != -1:
    gameAgent.run()

    

    
    


     
        

