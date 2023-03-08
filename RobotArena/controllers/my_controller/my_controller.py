"""my_controller controller."""
from ArmController import armcontroll
from controller import Robot
from ArmPositionValues import shoulder_val,WAIST_VAL,wrist_val,pitch_val,elbow_val
# from Robotclass import run_robot2

def run_robot(robot):
    max_velocity=0
    timestep = int(robot.getBasicTimeStep())
    arm=armcontroll(robot)
    while robot.step(timestep) != -1:
        arm.collectbox(WAIST_VAL,shoulder_val,elbow_val,wrist_val,pitch_val)
        #arm.putinback(-11,0,0,0,0)
        pass

if __name__ =="__main__":
    my_robot=Robot()
    run_robot(my_robot)
