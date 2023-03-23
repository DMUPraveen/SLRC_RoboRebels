from controller import Robot


class GrabBox:
    def __init__(self, robot: Robot):
        self.robot = robot

        self.motor_1 = self.robot.getDevice("slider_motor1")
        self.motor_2 = self.robot.getDevice("slider_motor2")

    def grab(self):
        self.motor_1.setPosition(-0.04)
        self.motor_1.setVelocity(0.1)
        self.motor_2.setPosition(0.02)
        self.motor_2.setVelocity(0.1)

    def release(self):
        self.motor_1.setPosition(0)
        self.motor_1.setVelocity(0.1)
        self.motor_2.setPosition(-0.1)
        self.motor_2.setVelocity(0.1)

    def stop(self):
        self.motor_1.setPosition(-0.04)
        self.motor_1.setVelocity(0.01)
        self.motor_2.setPosition(0.02)
        self.motor_2.setVelocity(0.01)
