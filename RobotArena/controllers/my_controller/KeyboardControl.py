from controller import Keyboard
from ArmController import armcontroll

arm=armcontroll
VELOCITY = 0.1
keyboard_control_on = True
CONTROL_KEY = ord('Q')
actions = {
    ord('A'): lambda arm: arm.waistcontrol(arm, VELOCITY),
    ord('D'): lambda arm: arm.shouldercontrol(arm, VELOCITY),
    ord('S'): lambda arm: arm.elbowcontrol(arm,VELOCITY),
    ord('W'): lambda arm: arm.wristcontrol(arm,VELOCITY),
    ord('B'): lambda arm: arm.pitchcontrol(arm,VELOCITY)
}


def control_arm_via_keyboard(keyboard: Keyboard, arm: arm):
    key = None
    global keyboard_control_on
    key = keyboard.getKey()
    if(key == CONTROL_KEY):
        keyboard_control_on = not(keyboard_control_on)
    if(not keyboard_control_on):
        return
    if(key in actions):
        actions[key](arm)
        return

    arm.stoparm()