from controller import Robot


class GrabBox:
    def __init__(self, robot: Robot):
        self.robot = robot

        self.motor_1 = self.robot.getDevice("slider_motor1")
        self.motor_2 = self.robot.getDevice("slider_motor2")
        self.down_motor=self.robot.getDevice("down_motor")

    def grab(self):
        self.motor_1.setPosition(-0.04)
        self.motor_1.setVelocity(0.05)
        self.motor_2.setPosition(0.02)
        self.motor_2.setVelocity(0.05)

    def release(self):
        self.motor_1.setPosition(0)
        self.motor_1.setVelocity(0.05)
        self.motor_2.setPosition(-0.1)
        self.motor_2.setVelocity(0.05)

    def stop(self):
        self.motor_1.setPosition(-0.04)
        self.motor_1.setVelocity(0.005)
        self.motor_2.setPosition(0.02)
        self.motor_2.setVelocity(0.005)

    def upmotor(self):
        self.down_motor.setPosition(0.01)
        self.down_motor.setVelocity(0.01)
