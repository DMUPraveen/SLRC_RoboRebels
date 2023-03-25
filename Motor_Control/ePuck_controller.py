"""ePuck_controller controller."""

import sys

# sys.path.insert(0,'C:\\Users\\msi\\Desktop\\SLRC_RoboRebels\\deploy_scripts')

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
# import main
from RobotManagerScript import RobotManager as RM
# from D_GAScript import D_GA
import numpy as np
# import cv2

robot = RM()
timestep = robot.timeStep

# gameAgent = D_GA(robot)

while robot.step(timestep) != -1:
    # gameAgent.run()
    

    obsWidth = 5 #Assign the value
    ultrasonicStatus = False

    if RM.get_ultrasonic_distances[1] < 1:
        ultrasonicStatus = True  #True if detects an obstacle

    def obsAvoidAlgo():
        while ultrasonicStatus == False:
            RM.move_forward()

        if ultrasonicStatus == True:
            if RM.get_ultrasonic_distances[2] < RM.get_ultrasonic_distances[0]:
                RM.turn_left()
                distToWall = ultrasonicReading
                while distToWall - RM.get_ultrasonic_distances[1] < 0.06:
                    RM.move_forward()

                RM.turn_right()
                obsAvoidAlgo()

            else:
                RM.turn_right()
                distToWall = ultrasonicReading
                while distToWall - RM.get_ultrasonic_distances[1] < 5:
                    RM.move_forward()
                
                RM.turn_left()
                obsAvoidAlgo()
            
        # if finishLineDitected == True:
        #     stop()
        #     return 0

    

    
    


     
        

