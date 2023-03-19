""" Controls All Box Collecting Algorithms"""

from controller import Robot
from SuperArm import Armstatemachine
from Boxdetector import BoxDetector

class SuperState:
    def __init__(self,robot:Robot,superarmcontroller:Armstatemachine,boxdetector:BoxDetector):
        self.robot=Robot()
        self.superarm=superarmcontroller
        self.boxdetector=boxdetector

        self.state=0

    def SuperStateMachine(self):
        if self.state==0 and self.boxdetector.setposition():
            self.state=1

        if self.state==1 and self.superarm.pickupbox():
            self.state=2

        print(self.state)
