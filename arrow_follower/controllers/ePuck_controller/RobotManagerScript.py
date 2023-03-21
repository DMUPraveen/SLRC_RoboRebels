from controller import Robot
import cv2
import numpy as np

max_velocity = np.pi*2

class RobotManager(Robot):

    def __init__(self):
        Robot.__init__(self)
        self.timeStep = int(self.getBasicTimeStep())
        self.initialize_all_sensors();
    
    
    def initialize_all_sensors(self):
        #Motors
        self.left_motor = self.getDevice("left motor")
        self.right_motor = self.getDevice("right motor")
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

        # US 
        self.left_US = self.getDevice("leftUS")
        self.right_US = self.getDevice("rightUS")
        self.front_US = self.getDevice("frontUS")

        self.left_US.enable(self.timeStep)
        self.right_US.enable(self.timeStep)
        self.front_US.enable(self.timeStep)

        self.US_sensors = [self.left_US, self.front_US, self.right_US]

        #Distance Sensors
        self.ds0 = self.getDevice("DS0")
        self.ds1 = self.getDevice("DS1")
        self.ds2 = self.getDevice("DS2")
        self.ds3 = self.getDevice("DS3")
        self.ds4 = self.getDevice("DS4")
        self.ds5 = self.getDevice("DS5")

        self.ds0.enable(self.timeStep)
        self.ds1.enable(self.timeStep)
        self.ds2.enable(self.timeStep)
        self.ds3.enable(self.timeStep)
        self.ds4.enable(self.timeStep)
        self.ds5.enable(self.timeStep)

        self.DS_sensors = [self.ds0, self.ds1, \
                           self.ds2, self.ds3, self.ds4, self.ds5]

        #Camera
        self.cam = self.getDevice("rebelEye")
        self.cam.enable(self.timeStep)


    def get_ultrasonic_distances(self):
        US_distances = []
        for sensor in self.US_sensors:
            US_distances.append(sensor.getValue())
        return np.array(US_distances)


    def get_camera_feed(self):
        cameraData = self.cam.getImage()

        image = np.frombuffer(cameraData, np.uint8).\
            reshape((self.cam.getHeight(), self.cam.getWidth(), 4))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def get_line_sensor_val(self):
        ds_distances = []
        for sensor in self.DS_sensors:
            ds_distances.append(sensor.getValue())
        return np.array(ds_distances)

    def move_forward(self):
        self.left_motor.setVelocity(0.8*max_velocity)
        self.right_motor.setVelocity(0.8*max_velocity)

