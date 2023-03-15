from controller import Robot

class armcontroll:
    def __init__(self,robot:Robot):
        self.robot=robot
        self.TIME_STEP=32
        self.velocity=0.2

        #arm components
        self.waist_motor = robot.getDevice('waist_motor')
        self.shoulder_motor = robot.getDevice('shoulder_motor')
        self.elbow_motor = robot.getDevice('elbow_motor')
        self.wrist_motor = robot.getDevice('wrist_motor')
        self.pitch_motor = robot.getDevice('pitch_motor')

        self.finger_motor_right = robot.getDevice('right_finger_motor')
        #self.finger_motor_left = robot.getDevice('left_finger_motor')

       

    def waistcontrol(self,waist_val):
        self.waist_motor.setPosition(waist_val)
        self.waist_motor.setVelocity(0.5)
        self.robot.step(30*self.TIME_STEP)

    def shouldercontrol(self,shoulder_val):
        self.shoulder_motor.setPosition(shoulder_val)
        self.shoulder_motor.setVelocity(0.15)
        self.robot.step(100*self.TIME_STEP)
        self.shoulder_motor.setVelocity(0)

    def elbowcontrol(self,elbow_val):
        self.elbow_motor.setPosition(elbow_val)
        self.elbow_motor.setVelocity(0.5)
        self.robot.step(50*self.TIME_STEP)

    def wristcontrol(self,wrist_val):
        self.wrist_motor.setPosition(wrist_val)
        self.wrist_motor.setVelocity(0.5)
        self.robot.step(30*self.TIME_STEP)
    
    def pitchcontrol(self,pitch_val):
        self.pitch_motor.setPosition(pitch_val)
        self.pitch_motor.setVelocity(0.5)
        self.robot.step(30*self.TIME_STEP)

    def initialfingers(self):
        self.finger_motor_right.setPosition(float('inf'))
        self.finger_motor_right.setVelocity(1)
        #self.finger_motor_left.setPosition(-1)
        # self.finger_motor_left.setVelocity(1)

    def stoparm(self):
        # self.shoulder_motor.setVelocity(0)
        self.elbow_motor.setVelocity(0)
        self.wrist_motor.setVelocity(0)
        self.pitch_motor.setVelocity(0)
        self.waist_motor.setVelocity(0)


    def collectbox(self,waist_val,shoulder_val,elbow_val,wrist_val,pitch_val):
        self.waistcontrol(waist_val)
        self.elbowcontrol(elbow_val)
        self.shouldercontrol(shoulder_val)
        self.pitchcontrol(pitch_val)
        self.wristcontrol(wrist_val)
        self.robot.step(50*self.TIME_STEP)
        self.stoparm()

    def hangbox(self):
        self.initialfingers()
        self.robot.step(10*self.TIME_STEP)
        self.shoulder_motor.setPosition(0)
        self.shoulder_motor.setVelocity(0.35)
        self.robot.step(20*self.TIME_STEP)



    def putinback(self,waist_val,shoulder_val,elbow_val,wrist_val,pitch_val):
        self.shouldercontrol(shoulder_val)
        self.waistcontrol(waist_val)
        self.pitchcontrol(pitch_val)
        self.elbowcontrol(elbow_val)
        self.wristcontrol(wrist_val)
        self.robot.step(50*self.TIME_STEP)
        self.stoparm()
        
        
        

