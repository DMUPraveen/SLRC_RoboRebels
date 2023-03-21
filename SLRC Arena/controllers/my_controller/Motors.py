from controller import Robot


class Motorcontrol:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.maxvelocity = -3
        self.left_motor1 = self.robot.getMotor("Left_motor1")
        self.right_motor1 = self.robot.getMotor("Right_motor1")
        self.left_motor1.setPosition(float('inf'))
        self.right_motor1.setPosition(float('inf'))
        self.left_motor1.setVelocity(0)
        self.right_motor1.setVelocity(0)

        self.linear_speed = 0.0
        self.rotational_speed = 0.0

    def setspeed(self, left_motor_v, right_motor_v):
        # left_motor_v=left_motor_v*self.maxvelocity
        # right_motor_v=right_motor_v*self.maxvelocity
        self.left_motor1.setVelocity(left_motor_v)
        self.right_motor1.setVelocity(right_motor_v)

    def simpleforward(self):
        self.left_motor1.setVelocity(self.maxvelocity)
        self.right_motor1.setVelocity(self.maxvelocity)

    def simpleturnleft(self):
        self.left_motor1.setVelocity(-self.maxvelocity)
        self.right_motor1.setVelocity(self.maxvelocity)

    def simplestop(self):
        self.left_motor1.setVelocity(0)
        self.right_motor1.setVelocity(0)

    def set_pose_speed(self):
        self.setspeed(self.linear_speed+self.rotational_speed,
                      self.linear_speed-self.rotational_speed)
