"""my_controller controller."""
from ArmController import armcontroll
from controller import Robot, Supervisor
from PositionSensors import Positions
from SuperArm import Armstatemachine
from Motors import Motorcontrol
from Boxdetector import BoxDetector
from SuperStateMachineForCatchTheBox import SuperState
from CameraClass import Camera
from HanoiPlace import Hanoi


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
    Hano=Hanoi(robot,arm,pos)
    
    while robot.step(timestep) != -1:
        # cam.alignwithbox()
        # arm.releasefingers()
        superduper.SuperStateMachine()

        # print(cam.isAligned())
            # Hano.StateMachineForHanoiPlace(1)
        pass

# if __name__=="__main__":
#     main()


    

