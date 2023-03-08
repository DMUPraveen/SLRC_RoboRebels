from controller import Robot
from controller import Motor


class Res:
    def __init__(self):
        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())

        self.keyboard = self.robot.getKeyboard()
        self.keyboard.enable(self.timestep)

        self.waist_motor: Motor = self.robot.getMotor('waist_motor')
        self.shoulder_motor: Motor = self.robot.getMotor('shoulder_motor')
        self.elbow_motor: Motor = self.robot.getMotor('elbow_motor')
        self.wrist_motor: Motor = self.robot.getMotor('wrist_motor')
        self.pitch_motor: Motor = self.robot.getMotor('pitch_motor')

        self.waist_motor.setPosition(float("inf"))
        self.shoulder_motor.setPosition(float("inf"))
        self.elbow_motor.setPosition(float("inf"))
        self.wrist_motor.setPosition(float("inf"))
        self.pitch_motor.setPosition(float("inf"))
        
        self.waist_motor.setVelocity(0)
        self.shoulder_motor.setVelocity(0)
        self.elbow_motor.setVelocity(0)
        self.wrist_motor.setVelocity(0)
        self.pitch_motor.setVelocity(0)