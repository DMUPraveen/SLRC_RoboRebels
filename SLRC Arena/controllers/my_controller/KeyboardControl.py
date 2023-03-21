from controller import Keyboard
from typing import Callable, Dict, List
from collections import defaultdict
from Motors import Motorcontrol


class KeyboardControl:
    def __init__(self, keyboard: Keyboard, sampling_time: int):
        self.actions: Dict[int, List[Callable[[], None]]
                           ] = defaultdict(lambda: [])

        self.keyboard = keyboard
        keyboard.enable(sampling_time)

    def register_action(self, key: str, action: Callable[[], None]):
        self.actions[ord(key)].append(action)

    def execute(self):
        while True:
            key = self.keyboard.getKey()
            if(key == -1):
                break
            for action in self.actions[key]:
                action()


def get_control_actions(motor_control: Motorcontrol):
    def turn_left():
        motor_control.rotational_speed = 1

    def turn_right():
        motor_control.rotational_speed = -1

    def go_forward():
        motor_control.linear_speed = -10

    def go_back():
        motor_control.linear_speed = 10

    return turn_left, turn_right, go_forward, go_back


def create_normal_drive(keyboardControl: KeyboardControl, motorcontrol: Motorcontrol):
    turn_left, turn_right, go_forward, go_back = get_control_actions(
        motorcontrol)
    keyboardControl.register_action('A', turn_left)
    keyboardControl.register_action('D', turn_right)
    keyboardControl.register_action('W', go_forward)
    keyboardControl.register_action('S', go_back)
