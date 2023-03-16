from controller import Robot
from ArmController import armcontroll
from PositionSensors import Positions
from Motors import Motorcontrol
from ArmPositionValues import shoulder_val,WAIST_VAL,wrist_val,pitch_val,elbow_val

class Armstatemachine:
    def __init__(self,robot:Robot,armcontroller:armcontroll,positions:Positions,motorcontroller:Motorcontrol):
        self.state=0
        self.robot=robot
        self.TIME=0
        self.TIME_THRESHOLD=100
        self.pos=positions
        self.arm=armcontroller
        self.car=motorcontroller

    def pickupbox(self):
        if (self.pos.isPositioned() and self.state==0):
            self.state=1

        if self.state==1 and self.pos.isCaught():
            self.state=2
        if(self.state ==2 and self.TIME >self.TIME_THRESHOLD):
            self.state=3
            self.TIME=0
        if self.state==3 and self.pos.isHung():
            self.state=4
        if self.state==4 and self.pos.isPlaced():
            self.state=5

        if self.state==0:
            self.arm.collectbox(WAIST_VAL,shoulder_val,elbow_val,wrist_val,pitch_val)
            print("running State0")
        if self.state==1:
            self.arm.catchbox()
        if self.state==2:
            self.TIME+=1
        if self.state ==3:
            self.arm.bringup()
        if self.state ==4:
            self.arm.putinback(-11,-0.8,-1,0,-1.3)
        if self.state==5:
            self.state=-1
            return True
        print(self.state)
    
