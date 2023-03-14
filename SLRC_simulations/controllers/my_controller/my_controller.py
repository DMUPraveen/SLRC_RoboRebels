"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,DistanceSensor

def run_robot(robot):
   
    timestep = int(robot.getBasicTimeStep())
    linesensor1:DistanceSensor =robot.getDevice("linesensor(1)")
    linesensor1.enable(timestep)


    while robot.step(timestep) != -1:
        print(linesensor1.getValue())
        pass

if __name__ =="__main__":
    my_robot=Robot()
    run_robot(my_robot)
    pass
