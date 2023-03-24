from controller import Robot


class GrabBox:
    def __init__(self, robot: Robot):
        self.robot = robot

        self.motor_1 = self.robot.getDevice("slider_motor1")
        self.motor_2 = self.robot.getDevice("slider_motor2")
        self.down_motor=self.robot.getDevice("down_motor")
        self.motor_3 = self.robot.getDevice("slider_motor3")
        self.motor_4 = self.robot.getDevice("slider_motor4")

    def grab(self):
        self.motor_1.setPosition(-0.04)
        self.motor_1.setVelocity(0.02)
        self.motor_2.setPosition(0.02)
        self.motor_2.setVelocity(0.02)

    def grab_side(self):
        return
        self.motor_3.setPosition(-0.03)
        self.motor_3.setVelocity(0.02)
        self.motor_4.setPosition(0.03)
        self.motor_4.setVelocity(0.02)


    def release(self):
        self.motor_1.setPosition(0)
        self.motor_1.setVelocity(0.05)
        self.motor_2.setPosition(-0.01)
        self.motor_2.setVelocity(0.05)
        self.motor_3.setPosition(0)
        self.motor_3.setVelocity(0.05)
        self.motor_4.setPosition(0)
        self.motor_4.setVelocity(0.05)

    def stop(self):
        self.motor_1.setPosition(-0.04)
        self.motor_1.setVelocity(0.005)
        self.motor_2.setPosition(0.02)
        self.motor_2.setVelocity(0.005)
        self.motor_3.setVelocity(0.005)
        self.motor_4.setVelocity(0.005)

    def upmotor(self):
        self.down_motor.setPosition(0.015)
        self.down_motor.setVelocity(0.01)

    def downmotor(self):
        self.down_motor.setPosition(0)
        self.down_motor.setVelocity(0)
