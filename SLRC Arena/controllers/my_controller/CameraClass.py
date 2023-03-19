from controller import Robot
import numpy as np
import cv2
from Motors import Motorcontrol

class Camera:
    def __init__(self,robot:Robot,motorcontroller:Motorcontrol):
        self.robot=robot
        self.car=motorcontroller
        self.TIME_STEP=64
        self.kBlurSize = 5

        self.cam= robot.getDevice('rebelEye')
        self.enableCamera()
    
    def enableCamera(self):
        self.cam.enable(self.TIME_STEP)

    def extractChannel(self,hsv, color):

        if color=='R':
            # define the range of red color in HSV color space
            lower_red_1 = np.array([0, 50, 50])
            upper_red_1 = np.array([10, 255, 255])
            lower_red_2 = np.array([170, 50, 50])
            upper_red_2 = np.array([180, 255, 255])

            # extract the red color from the HSV image
            red_mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
            red_mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
            mask = cv2.bitwise_or(red_mask_1, red_mask_2)
        elif color=='G':
            # define the range of green color in HSV color space
            lower_green = np.array([40, 50, 50])
            upper_green = np.array([80, 255, 255])

            # extract the green color from the HSV image
            mask = cv2.inRange(hsv, lower_green, upper_green)
        elif color=='B':
            # define the range of blue color in HSV color space
            lower_blue = np.array([100, 150, 50])
            upper_blue = np.array([140, 255, 255])

            # extract the blue color from the HSV image
            mask = cv2.inRange(hsv, lower_blue, upper_blue)   

        return mask


    def get_centeroid(self,channel, imgV=False):

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(channel, (self.kBlurSize, self.kBlurSize), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(blurred, 50, 200)

        

        # Perform Hough transform
        error_factor = 1
        image_perimeter = np.where(edges>0)
        perimeter = len(image_perimeter[0])
        if perimeter<5:
            return False, (0,0)

        y = int(np.sum(image_perimeter[0])/perimeter)
        x = int(np.sum(image_perimeter[1])/perimeter)
                
        if imgV:
            cv2.imshow('Canny Edges', edges)
            cv2.circle(edges, (x, y), radius=1, color=(255, 255, 255), thickness=-1)
            cv2.imshow("With Centeroid", edges)
            cv2.waitKey(self.TIME_STEP)

        return True,(x,y)


    def ErrorCalibration(self,verb=True, imageVerbose= False):

        cameraData = self.cam.getImage()

        image = np.frombuffer(cameraData, np.uint8).reshape((self.cam.getHeight(), self.cam.getWidth(), 4))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        red_channel = self.extractChannel(image, 'R')
        blue_channel = self.extractChannel(image, 'B')
        green_channel =  self.extractChannel(image, 'G')
 
        if imageVerbose:
            cv2.imshow('Blue', blue_channel)
            cv2.imshow('Green', green_channel)
            cv2.imshow('Blue', blue_channel)
            cv2.waitKey(self.TIME_STEP)

        #Get the centeroids of the individual blobs
        red_center = self.get_centeroid(red_channel,imgV=imageVerbose)
        blue_center = self.get_centeroid(blue_channel, imgV=imageVerbose)
        green_center = self.get_centeroid(green_channel,imgV=imageVerbose)

        redDet = 0
        greenDet = 0
        blueDet = 0

        error_blue=0
        error_red=0
        error_green=0

        Error=None

        if blue_center[0]:
            error_blue = (image.shape[1]/2)-blue_center[1][0]
            blueDet = 1

        if red_center[0]:
            error_red = (image.shape[1]/2)-red_center[1][0]
            redDet = 1
        if green_center[0]:
            error_green = (image.shape[1]/2)-green_center[1][0]
            greenDet = 1
        
        if verb:
            print("Red %i \t Green %i \t Blue %i"%(redDet, greenDet, blueDet),end='\t')
        if redDet:
            print('Red @', red_center,end='\t') if verb else 0
            Error=error_red
        if greenDet:
            print('Green @', green_center,end='\t') if verb else 0
            Error=error_green
        if blueDet:
            print('Blue @', blue_center,'Error :',Error) if verb else 0
            Error=error_blue
        print(Error)
        return Error
    
    def alignwithbox(self):
        print("RUNNING CAMERA")
        error=self.ErrorCalibration()
        if error:
            speed = 0.009*error
            self.car.setspeed(+speed,-speed)
            return error
        

    def isAligned(self):
        error=self.ErrorCalibration()
        if error==0:
            self.car.simplestop()
            print("TEST PASSED")
            return True
        
        # leftMotor.setVelocity(+speed)
        # rightMotor.setVelocity(-speed)



