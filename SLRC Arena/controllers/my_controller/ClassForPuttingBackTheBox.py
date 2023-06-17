from controller import Robot
from ArmController import armcontroll
from PositionSensors import Positions

class PutTHEDAMNBOX:
    def __init__(self,robot:Robot,armcontroller:armcontroll,positions:Positions):
        self.robot=robot
        self.arm=armcontroller
        self.pos=positions
        self.state=0

    def StateMaching_PUTTHEDAMN_1st_BOX(self):
        if self.state==0:
            self.arm.bringup()

        if self.state==1:
            self.arm.hanoiPlaceBottom(-11, 1.5, 1.8, 0, -1.75)


        if self.state==0 and self.pos.isHung():
            self.state=1

        if self.state==1 and self.pos.isHanoiBottomPlaced():
            self.state=0
            return True
        return False