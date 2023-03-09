"""my_controller controller."""
from ArmController import armcontroll
from controller import Robot
from ArmPositionValues import shoulder_val,WAIST_VAL,wrist_val,pitch_val,elbow_val
from KeyboardControl import control_arm_via_keyboard
from Resources import Res
from communi import new_arm


def main():
    robot=Robot()
    max_velocity=0
    timestep = int(robot.getBasicTimeStep())
    arm=armcontroll(robot)
    while robot.step(timestep) != -1:
        arm.collectbox(WAIST_VAL,shoulder_val,elbow_val,wrist_val,pitch_val)
        #arm.hangbox()
        arm.putinback(-11,0,0,0,0)
        pass

# if __name__=="__main__":
#     main()


    

