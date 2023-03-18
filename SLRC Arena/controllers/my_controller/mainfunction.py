"""my_controller controller."""
from ArmController import armcontroll
from controller import Robot, Supervisor
from PositionSensors import Positions
from SuperArm import Armstatemachine
from Motors import Motorcontrol
from Boxdetector import BoxDetector


def main():
    robot=Robot()
    timestep = int(robot.getBasicTimeStep())
    arm=armcontroll(robot)
    car=Motorcontrol(robot)
    pos=Positions(robot,arm)
    superarm=Armstatemachine(robot,arm,pos,car)
    boxdetect=BoxDetector(robot,car)
    while robot.step(timestep) != -1:
        boxdetect.setposition()
        # superarm.pickupbox()
        pass

# if __name__=="__main__":
#     main()


    

