from ArmController import armcontroll
from Resources import Res

def new_arm(arm :armcontroll,Res : Res):
    Res.waist_motor.setVelocity(arm.velocity)
    Res.shoulder_motor.setVelocity(arm.velocity)
    Res.elbow_motor.setVelocity(arm.velocity)
    Res.wrist_motor.setVelocity(arm.velocity)
    Res.pitch_motor.setVelocity(arm.velocity)