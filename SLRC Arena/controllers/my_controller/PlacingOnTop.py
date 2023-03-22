from controller import Robot
from ArmController import armcontroll
from PositionSensors import Positions
from Motors import Motorcontrol
from Boxdetector import BoxDetector

class Hanoi:
    def __init__(self,robot:Robot,armcontroller:armcontroll,positioncontroller:Positions,boxdetector:BoxDetector,motorcontroller:Motorcontrol):
        self.state=0
        self.robot=robot
        self.arm=armcontroller
        self.pos=positioncontroller
        self.boxDetector=boxdetector
        self.TIME=0
        self.TIME_THRESHOLD=100
        self.car=motorcontroller

    def PlacingFirstBox(self):
        self.arm.hanoiPlaceBottom(-11,1.5,1.8,0,-1.75)


    def PlacingSecondBox(self):
        self.arm.hanoiPlace_1_top(-11,0.7,2.4,0,-1.5) #### Change

    def PlacingThirdBox(self):
        self.arm.hanoiPlace_2_top_top(-11,0,2.4,0,-0.9)  #### Change

    def BuildHanoi(self,position):
        if self.state<4:
            self.arm.catchbox()
        if position==1:
            print("BOTTOM")
            self.PlacingFirstBox()
            if self.pos.isHanoiBottomPlaced():
                self.state=1

        else:
            if position==2:
                if self.state==0 and self.pos.isHanoi_top_1_Placed():
                    self.state=1

                if self.state==0:
                    self.PlacingSecondBox()


            if position==3:
                if self.state==0:
                    self.PlacingThirdBox()

                if self.state==0 and self.pos.isHanoi_top_2_Placed():
                    self.state=1
                


        if(self.state ==1 and self.TIME >self.TIME_THRESHOLD):
                self.state=2

        if self.state==1:
                self.TIME+=1
                self.arm.releasefingers()
                print(self.TIME)

        if self.state==2:
            self.arm.releasefingers()
            self.car.setspeed(1,1)
        print(self.state)