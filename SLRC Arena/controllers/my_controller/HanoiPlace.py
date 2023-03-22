from controller import Robot
from ArmController import armcontroll
from PositionSensors import Positions

class Hanoi:
    def __init__(self,robot:Robot,armcontroller:armcontroll,positioncontroller:Positions):
        self.state=0
        self.robot=robot
        self.arm=armcontroller
        self.pos=positioncontroller
        self.arm.catchbox()


    def StateMachineForHanoiPlace(self,position): ##Position--> place where to place the box
        if self.state==0:
            self.arm.bringup()

        if self.state==1 and position==1:
            self.arm.hanoiPlaceBottom(-11,0.5,2.2,0,0.15)

        if self.state==1 and position==2:
            self.arm.catchbox()
            self.arm.hanoiPlace_1_top(-11,0.5,2.2,0,0.15)

        if self.state==2:
            self.arm.releasefingers()


        if self.state==0 and self.pos.isHung():
            self.state=1

        if self.state==1 and self.pos.isHanoiBottomPlaced():
            self.state=2


                