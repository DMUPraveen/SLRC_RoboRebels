from controller import Robot


class armcontroll:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.TIME_STEP = 32
        self.velocity = 0.2

        # arm components
        self.waist_motor = robot.getMotor('waist_motor')
        self.shoulder_motor = robot.getMotor('shoulder_motor')
        self.elbow_motor = robot.getMotor('elbow_motor')
        self.wrist_motor = robot.getMotor('wrist_motor')
        self.pitch_motor = robot.getMotor('pitch_motor')

        self.finger_motor_right = robot.getMotor('right_finger_motor')
        self.finger_motor_left = robot.getMotor('left_finger_motor')

    def releasefingers(self):
        self.finger_motor_right.setVelocity(0.7)
        self.finger_motor_right.setPosition(0)
        self.finger_motor_left.setVelocity(0.7)
        self.finger_motor_left.setPosition(0)

    def catchbox(self):
        self.finger_motor_right.setPosition(-1)
        self.finger_motor_right.setVelocity(0.7)
        self.finger_motor_left.setPosition(1)
        self.finger_motor_left.setVelocity(0.7)
        # self.robot.step(50*self.TIME_STEP)

    def waistcontrol(self, waist_val):
        self.waist_motor.setPosition(waist_val)
        self.waist_motor.setVelocity(0.5)
        # self.robot.step(30*self.TIME_STEP)

    def shouldercontrol(self, shoulder_val):
        self.shoulder_motor.setPosition(shoulder_val)
        self.shoulder_motor.setVelocity(0.15)
        # self.robot.step(80*self.TIME_STEP)

    def elbowcontrol(self, elbow_val):
        self.elbow_motor.setPosition(elbow_val)
        self.elbow_motor.setVelocity(0.4)
        # self.robot.step(50*self.TIME_STEP)

    def wristcontrol(self, wrist_val):
        self.wrist_motor.setPosition(wrist_val)
        self.wrist_motor.setVelocity(0.5)
        # self.robot.step(30*self.TIME_STEP)

    def pitchcontrol(self, pitch_val):
        self.pitch_motor.setPosition(pitch_val)
        self.pitch_motor.setVelocity(0.4)
        # self.robot.step(30*self.TIME_STEP)

    def stoparm(self):
        self.shoulder_motor.setVelocity(0)
        self.elbow_motor.setVelocity(0)
        self.wrist_motor.setVelocity(0)
        self.pitch_motor.setVelocity(0)
        self.waist_motor.setVelocity(0)

    def collectbox(self, waist_val, shoulder_val, elbow_val, wrist_val, pitch_val):
        self.waistcontrol(waist_val)
        self.elbowcontrol(elbow_val)
        self.shouldercontrol(shoulder_val)
        self.pitchcontrol(pitch_val)
        # self.releasefingers()
        # self.catchbox()
        # self.wristcontrol(wrist_val)

    def putinback(self, waist_val, shoulder_val, elbow_val, wrist_val, pitch_val):
        self.shouldercontrol(shoulder_val)
        self.pitchcontrol(pitch_val)
        self.elbowcontrol(elbow_val)
        self.wristcontrol(wrist_val)

    def bringup(self):
        self.shouldercontrol(0)
        self.pitchcontrol(0)
        self.elbowcontrol(0)
        self.wristcontrol(0)

    """ MOVE FORWARD TO THE BOX"""

    def takeelbow_pitch(self):
        self.elbowcontrol(1.55)
        self.pitchcontrol(-1.5)

    """ HANOI PLACEMENT"""

    def hanoiPlaceBottom(self, waist_val, shoulder_val, elbow_val, wrist_val, pitch_val):
        self.waistcontrol(waist_val)
        self.elbowcontrol(elbow_val)
        self.shouldercontrol(shoulder_val)
        self.pitchcontrol(pitch_val)

    def hanoiPlace_1_top(self, waist_val, shoulder_val, elbow_val, wrist_val, pitch_val):
        self.waistcontrol(waist_val)
        self.elbowcontrol(elbow_val)
        self.shouldercontrol(shoulder_val)
        self.pitchcontrol(pitch_val)

    def hanoiPlace_2_top_top(self, waist_val, shoulder_val, elbow_val, wrist_val, pitch_val):
        self.waistcontrol(waist_val)
        self.elbowcontrol(elbow_val)
        self.shouldercontrol(shoulder_val)
        self.pitchcontrol(pitch_val)

    """ ADDED BECAUSE PUTTING DOWN"""

    def Catch_BOX_For_PUTTING(self):
        self.finger_motor_right.setPosition(-2)
        self.finger_motor_right.setVelocity(3)
        self.finger_motor_left.setPosition(1)
        self.finger_motor_left.setVelocity(2)
