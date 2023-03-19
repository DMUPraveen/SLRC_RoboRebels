""" Controls All Box Collecting Algorithms"""

from controller import Robot
from SuperArm import Armstatemachine
from Boxdetector import BoxDetector
from CameraClass import Camera

class SuperState:
    def __init__(self,robot:Robot,superarmcontroller:Armstatemachine,boxdetector:BoxDetector,cameracontroller:Camera):
        self.state=0
        self.TIME=0
        self.TIME_THRESHOLD=200
        self.robot= robot
        self.superarm=superarmcontroller
        self.boxdetector=boxdetector
        self.cam=cameracontroller

    def SuperStateMachine(self):

        if self.state==0 and self.cam.isAligned():
            self.state=1

        if self.state==1 and self.boxdetector.setposition():
            self.state=2

        if self.state==2 and self.superarm.pickupbox():
            return True

        if self.state==0:
            self.cam.alignwithbox()



        print("MAIN FUNCTION STATE",self.state)
