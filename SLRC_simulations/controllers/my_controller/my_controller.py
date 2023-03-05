"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.


# get the time step of the current world.
def run_robot(robot):
    max_velocity=6.28
   
    timestep = int(robot.getBasicTimeStep())
    
    left_motor1 = robot.getDevice("Left_motor1")
    left_motor2 = robot.getDevice("Left_motor2")
    
    right_motor1 = robot.getDevice("Right_motor1")
    right_motor2 = robot.getDevice("Right_motor2")
    
    left_motor1.setPosition(float("inf"))
    left_motor2.setPosition(float("inf"))
    
    right_motor1.setPosition(float("inf"))
    right_motor2.setPosition(float("inf"))
    
    
    while robot.step(timestep) != -1:
        left_motor1.setVelocity(max_velocity)
        left_motor2.setVelocity(max_velocity)
        
        right_motor1.setVelocity(max_velocity)
        right_motor2.setVelocity(max_velocity)
        
        pass

if __name__ =="__main__":
    my_robot=Robot()
    run_robot(my_robot)
