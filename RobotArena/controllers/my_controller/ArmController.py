from controller import Robot

class armcontroll:
    def __init__(self,robot:Robot):
        self.robot=robot

        #arm components
        self.waist_motor = robot.getDevice('waist_motor')
        self.shoulder_motor = robot.getDevice('shoulder_motor')
        self.elbow_motor = robot.getDevice('elbow_motor')
        self.wrist_motor = robot.getDevice('wrist_motor')
        self.pitch_motor = robot.getDevice('pitch_motor')
        # self.claw_motor1 = robot.getDevice('phalanx_motor::right')
        # self.claw_motor2 = robot.getDevice('phalanx_motor::left')
        #::right


        #initialize
        # self.claw_motor1.setPosition(0)
        # self.claw_motor2.setPosition(0)

    def collectbox(self,waist_val,shoulder_val,elbow_val,wrist_val,pitch_val):
        self.waist_motor.setPosition(waist_val)
        self.shoulder_motor.setPosition(shoulder_val)
        self.elbow_motor.setPosition(elbow_val)
        self.wrist_motor.setPosition(wrist_val)
        self.pitch_motor.setPosition(pitch_val)