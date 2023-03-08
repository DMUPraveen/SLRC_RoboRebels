"""my_controller controller."""
from ArmController import armcontroll
from controller import Robot
from ArmPositionValues import shoulder_val,waist_val,wrist_val,pitch_val,elbow_val

def run_robot(robot):
    max_velocity=0
    timestep = int(robot.getBasicTimeStep())
    arm=armcontroll(robot)
    while robot.step(timestep) != -1:
        arm.collectbox(waist_val,shoulder_val,elbow_val,wrist_val,pitch_val)

        pass

if __name__ =="__main__":
    my_robot=Robot()
    run_robot(my_robot)
