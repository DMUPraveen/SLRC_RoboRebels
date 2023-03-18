from controller import Robot,DistanceSensor
from Motors import Motorcontrol

class BoxDetector:
    def __init__(self,robot:Robot,motorcontroller:Motorcontrol):
        self.robot=Robot()
        self.TIME_STEP=10
        self.car=motorcontroller

        self.Left_corner_box_sensor=robot.getDevice("box_sensor_side1.2")
        self.Left_box_sensor=robot.getDevice("box_sensor_side1")
        self.Middle_box_sensor=robot.getDevice("box_sensor_middle")
        self.Right_box_sensor=robot.getDevice("box_sensor_side2")
        self.Right_corner_box_sensor=robot.getDevice("box_sensor_side2.2")

        self.Left_corner_value=0
        self.Left_value=0
        self.Middle_value=0
        self.Right_value=0
        self.Right_corner_value=0

    def enablesensors(self):
        self.Left_box_sensor.enable(self.TIME_STEP)
        self.Middle_box_sensor.enable(self.TIME_STEP)
        self.Right_box_sensor.enable(self.TIME_STEP)
        self.Left_corner_box_sensor.enable(self.TIME_STEP)
        self.Right_corner_box_sensor.enable(self.TIME_STEP)

        self.Left_corner_value=self.Left_corner_box_sensor.getValue()
        self.Left_value=self.Left_box_sensor.getValue()
        self.Middle_value=self.Middle_box_sensor.getValue()
        self.Right_value=self.Right_box_sensor.getValue()
        self.Right_corner_value=self.Right_corner_box_sensor.getValue()


    def frac(self,reading):
        return 1/(reading+1)

    def errorfunction(self):
        alpha=10
        beta=1
        gamma=1
        delta=10
        error=alpha*self.frac(self.Left_corner_value)+beta*self.frac(self.Left_value)-gamma*self.frac(self.Right_value)-delta*self.frac(self.Right_corner_value)
        return error
    
    def setposition(self):
        superalpha=1000
        self.enablesensors()
        error=self.errorfunction()
        speed=superalpha*error
        print(speed)
        self.car.setspeed(speed,-speed)

    