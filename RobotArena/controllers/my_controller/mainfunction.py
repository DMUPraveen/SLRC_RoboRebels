"""my_controller controller."""
from ArmController import armcontroll
from controller import Robot,PositionSensor
from ArmPositionValues import shoulder_val,WAIST_VAL,wrist_val,pitch_val,elbow_val
from PositionSensors import Positions
from Motors import Motorcontrol

def main():
    robot=Robot()
    max_velocity=0
    timestep = int(robot.getBasicTimeStep())
    arm=armcontroll(robot)
    car=Motorcontrol(robot)
    state = 0
    pos=Positions(robot,arm)
    t=0
    time_threshold = 100
    while robot.step(timestep) != -1:
        # car.simpleforward()
        # continue
        if (pos.isPositioned() and state==0):
            state=1

        if state==1 and pos.isCaught():
            state=2
        if(state ==2 and t >time_threshold):
            state=3
            t=0
        if state==3 and pos.isHung():
            state=4
        if state==4 and pos.isPlaced():
            state=5

        if state==0:
            arm.collectbox(WAIST_VAL,shoulder_val,elbow_val,wrist_val,pitch_val)
            print("running State0")
        if state==1:
            arm.catchbox()
        if state==2:
            t+=1
        if state ==3:
            arm.bringup()
        if state ==4:
            arm.putinback(-11,-0.8,-1,0,-1.3)
        if state==5:
            car.simpleforward()
        print(state)
        pass
        # if(state == 0):
        #     arm.collectbox(WAIST_VAL,shoulder_val,elbow_val,wrist_val,pitch_val)
        # if(state == 1):
        #     ark
        # # arm.bringup()
        # # arm.putinback(-11,-1,-0.7,0,-1.3)
        # # arm.releasefingers()
        # # arm.bringup()
        # if(psosmnssd == ,da and state =0):
        #     state +=1


# if __name__=="__main__":
#     main()


    

