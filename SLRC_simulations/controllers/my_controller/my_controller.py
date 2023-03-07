"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

#initialize the arm 
def armInit(robot):
    timestep = int(robot.getBasicTimeStep())
    
    waist_motor = robot.getDevice('waist_motor')
    waist_motor.setPosition(float('inf'))
    waist_s = 1
    waist_d = 0.1
    waist_motor.setVelocity(waist_s * waist_d)
    
    shoulder_motor = robot.getDevice('shoulder_motor')
    shoulder_motor.setPosition(float('inf'))
    shoulder_s = 1
    shoulder_d = 0.1
    shoulder_motor.setVelocity(shoulder_s * shoulder_d)
    
    elbow_motor = robot.getDevice('elbow_motor')
    elbow_motor.setPosition(float('inf'))
    elbow_s = 1
    elbow_d = 0
    elbow_motor.setVelocity(elbow_s * elbow_d)
    
    wrist_motor = robot.getDevice('wrist_motor')
    wrist_motor.setPosition(float('inf'))
    wrist_s = 1
    wrist_d = 0
    wrist_motor.setVelocity(wrist_s * wrist_d)
    
    pitch_motor = robot.getDevice('pitch_motor')
    pitch_motor.setPosition(float('inf'))
    pitch_s = 1
    pitch_d = 0
    pitch_motor.setVelocity(pitch_s * pitch_d)
    
    claw_motor = robot.getDevice('phalanx_motor::right')
    claw_motor.setPosition(float('inf'))
    claw_s = 1
    claw_d = 0
    claw_motor.setVelocity(claw_s * claw_d)
    
    # Initialize the position sensors at the joints
    waist_p = robot.getDevice('waist_sensor')
    waist_p.enable(timestep)
    
    shoulder_p = robot.getDevice('shoulder_sensor')
    shoulder_p.enable(timestep)
    
    elbow_p = robot.getDevice('elbow_sensor')
    elbow_p.enable(timestep)
    
    wrist_p = robot.getDevice('wrist_sensor')
    wrist_p.enable(timestep)
    
    pitch_p = robot.getDevice('pitch_sensor')
    pitch_p.enable(timestep)
    
    fingers_p = robot.getDevice('phalanx_sensor')
    fingers_p.enable(timestep)
    
    finger_s = robot.getDevice('finger_sensor')
    finger_s.enable(timestep)    

# get the time step of the current world.
def run_robot(robot):
    max_velocity=-6.28
   
    timestep = int(robot.getBasicTimeStep())
    
    left_motor1 = robot.getDevice("Left_motor1")
    
    right_motor1 = robot.getDevice("Right_motor1")
    
    left_motor1.setPosition(float("inf"))
    
    right_motor1.setPosition(float("inf"))

    while robot.step(timestep) != -1:
        left_motor1.setVelocity(max_velocity)
        right_motor1.setVelocity(max_velocity)
        
        pass

if __name__ =="__main__":
    my_robot=Robot()
    armInit(my_robot)
    run_robot(my_robot)
