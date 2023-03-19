"""my_controller controller."""
from ArmController import armcontroll
from controller import Robot, Supervisor
from PositionSensors import Positions
from SuperArm import Armstatemachine
from Motors import Motorcontrol
from Boxdetector import BoxDetector
from SuperStateMachineForCatchTheBox import SuperState
from CameraClass import Camera


def main():
    robot=Robot()
    timestep = int(robot.getBasicTimeStep())
    arm=armcontroll(robot)
    car=Motorcontrol(robot)
    pos=Positions(robot,arm)
    superarm=Armstatemachine(robot,arm,pos,car)
    boxdetect=BoxDetector(robot,car)
    cam=Camera(robot,car)
    superduper=SuperState(robot,superarm,boxdetect,cam)
    
    while robot.step(timestep) != -1:
        # cam.alignwithbox()
        superduper.SuperStateMachine()
        # print(cam.isAligned())
        pass

# if __name__=="__main__":
#     main()


    

