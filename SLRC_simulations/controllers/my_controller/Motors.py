from controller import Robot

class Motorcontrol:
    def __init__(self,robot:Robot):
        self.robot = robot
        self.maxvelocity=6.28
        self.left_motor1 = self.robot.getMotor("Left_motor1")
        self.left_motor2 = self.robot.getMotor("Left_motor2")
        self.right_motor1 = self.robot.getMotor("Right_motor1")
        self.right_motor2 = self.robot.getMotor("Right_motor2")

    def setVelocity(self,left_motor_v,right_motor_v):
        left_motor_v=left_motor_v*self.maxvelocity
        right_motor_v=right_motor_v*self.maxvelocity
        self.left_motor1.setVelocity(left_motor_v)
        self.left_motor2.setVelocity(left_motor_v)

        self.right_motor1.setVelocity(right_motor_v)
        self.right_motor2.setVelocity(right_motor_v)

        