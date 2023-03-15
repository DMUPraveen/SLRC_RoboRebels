from controller import Robot

class Finger:
    def __init__(self,robot:Robot):
        self.robot=robot
        self.TIME_STEP=32
        self.finger_motor_right = robot.getMotor('right_finger_motor')
        self.finger_motor_left = robot.getMotor('left_finger_motor')
    
    def releasefingers(self):
        self.finger_motor_right.setPosition(0)
        self.finger_motor_left.setPosition(0)

    def catchbox(self):
        self.finger_motor_right.setPosition(-1)
        self.finger_motor_right.setVelocity(1)
        self.finger_motor_left.setPosition(1)
        self.finger_motor_left.setVelocity(1)
        self.robot.step(50*self.TIME_STEP)

