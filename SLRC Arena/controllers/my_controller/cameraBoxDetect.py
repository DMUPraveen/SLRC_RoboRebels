
from controller import Robot, Keyboard
import numpy as np
import cv2


def extractChannel(hsv, color):

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

kBlurSize = 5
def get_centeroid(channel, timestep=64, imgV=True):

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(channel, (kBlurSize, kBlurSize), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 200)

    

    # Perform Hough transform
    error_factor = 1
    image_perimeter = np.where(edges>0)
    perimeter = len(image_perimeter[0])
    if perimeter<5:
        return (-1,-1)

    y = int(np.sum(image_perimeter[0])/perimeter)
    x = int(np.sum(image_perimeter[1])/perimeter)
            
    if imgV:
        cv2.imshow('Canny Edges', edges)
        cv2.circle(edges, (x, y), radius=1, color=(255, 255, 255), thickness=-1)
        cv2.imshow("With Centeroid", edges)
        cv2.waitKey(timestep)

    return (x,y)

    



def main(verb=True, imageVerbose= True):

    robot = Robot()

    timestep = int(robot.getBasicTimeStep())

    leftMotor = robot.getDevice('Left_motor1')
    rightMotor = robot.getDevice('Right_motor1')

    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))

    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    cam = robot.getDevice('rebelEye')
    cam.enable(timestep)

    max_velocity = 0


    while robot.step(timestep) != -1:

        cameraData = cam.getImage()

        image = np.frombuffer(cameraData, np.uint8).reshape((cam.getHeight(), cam.getWidth(), 4))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # red_channel = extractChannel(image, 'R')
        blue_channel = extractChannel(image, 'B')
        # green_channel =  extractChannel(image, 'G')
        
        if imageVerbose:
            cv2.imshow('Blue', blue_channel)
            # cv2.imshow('Green', green_channel)
            # cv2.imshow('Blue', blue_channel)
            cv2.waitKey(timestep)

        #Get the centeroids of the individual blobs
        # red_center = get_centeroid(red_channel, timestep)
        blue_cener = get_centeroid(blue_channel, imgV=imageVerbose)
        # green_center = get_centeroid(green_channel)

        if blue_channel!=(-1,-1):
            error = (image.shape[1]/2)-blue_cener[0]
            if verb:
                print(blue_cener, error)

            #Align Centeroid to Blob
            speed = 0.009*error
            leftMotor.setVelocity(+speed)
            rightMotor.setVelocity(-speed)
            
    
        

    #get the largest blob