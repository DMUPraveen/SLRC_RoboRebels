"""ePuck_controller controller."""

import sys

sys.path.insert(0,'E:\\DEEE\\4th SEM\\SLRC 23\\root\\deploy_scripts')

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Keyboard
import main

import numpy as np
import cv2
# create the Robot instance.
robot = Robot()


# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


keyboard = Keyboard()
keyboard.enable(timestep)

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

view = robot.getDevice('display')


cam = robot.getDevice('camera')
cam.enable(timestep)
width = view.getWidth()
height = view.getHeight()

# create view node
print(width,height)
max_velocity = 5

# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # get the largest blob
    # check if all arrow features are present
    # if two successive attempts give the same bearing drive to the centeroid
    # else move towards the centeroid by trying to bring the centeroid 
    # to the midpoint of the bottom edge

    #process image from camera 
    cameraData = cam.getImage()

    image = np.frombuffer(cameraData, np.uint8).reshape((cam.getHeight(), cam.getWidth(), 4))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageSize = image.shape[0]*image.shape[1]

    dis = main.get_bearing(image)

    cv2.imshow('tt', dis)
    cv2.waitKey(timestep)

    # Get keyboard input
    key = keyboard.getKey()
    # Change motor velocities based on keyboard input
    if key == Keyboard.UP:
        leftMotor.setVelocity(max_velocity)
        rightMotor.setVelocity(max_velocity)
    elif key == Keyboard.DOWN:
        leftMotor.setVelocity(-max_velocity)
        rightMotor.setVelocity(-max_velocity)
    elif key == Keyboard.RIGHT:
        leftMotor.setVelocity(max_velocity)
        rightMotor.setVelocity(-max_velocity)
    elif key == Keyboard.LEFT:
        leftMotor.setVelocity(-max_velocity)
        rightMotor.setVelocity(max_velocity)
    else:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)        

    #get the largest blob
