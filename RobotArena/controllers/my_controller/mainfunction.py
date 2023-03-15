"""my_controller controller."""
from ArmController import armcontroll
from controller import Robot
from ArmPositionValues import shoulder_val,WAIST_VAL,wrist_val,pitch_val,elbow_val

def main():
    robot=Robot()
    max_velocity=0
    timestep = int(robot.getBasicTimeStep())
    arm=armcontroll(robot)
    # finger=Finger(robot)
    while robot.step(timestep) != -1:
        arm.collectbox(WAIST_VAL,shoulder_val,elbow_val,wrist_val,pitch_val)
        arm.bringup()
        arm.putinback(-11,-1,-0.7,0,-1.3)
        # arm.releasefingers()
        # arm.bringup()


# if __name__=="__main__":
#     main()


    

