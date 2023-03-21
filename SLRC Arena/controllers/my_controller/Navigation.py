
from Motors import Motorcontrol
from DistanceSensors import DistanceSensors
from PID import PID


class Navigation:
    def __init__(self, motorController: Motorcontrol, distanceSensors: DistanceSensors):
        self.motorController = motorController
        self.distanceSensors = distanceSensors
        self.left_aling_pid = PID(30, 0, 0)
        self.right_aling_pid = self.left_aling_pid.create_copy()
        self.left_aling_pid.set_set_point(0)
        self.right_aling_pid.set_set_point(0)

    def align_to_left_wall(self):
        '''
        aligns to left wall does not check whether both sensor are engaged 
        returns the error
        this does not the motor velocity but the pose, motorsController.pose_control()
        must be called in order to activated this
        '''
        measurement = self.distanceSensors.left_wall_align_error()
        control_signal = self.left_aling_pid(measurement)
        self.motorController.rotational_speed = -control_signal
        return measurement

    def align_to_right_wall(self):
        '''
        aligns to right wall does not check whether both sensor are engaged 
        returns the error
        this does not the motor velocity but the pose, motorsController.pose_control()
        must be called in order to activated this
        '''
        measurement = self.distanceSensors.right_wall_align_error()
        control_signal = self.right_aling_pid(measurement)
        self.motorController.rotational_speed = -control_signal
        return measurement
