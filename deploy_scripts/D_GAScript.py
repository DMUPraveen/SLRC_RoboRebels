from finite_state_machine import FiniteStateMachine, FiniteStateMachineManager
import feature_extractor
import preprocessor
import cv2
import numpy as np

class D_GA():
    """
    Game Agent for Region D
    """
    def __init__(self, robot):
        """
        Create a finite state machine.

        Args:
            states (list): List of states.
            initial_state (str): Initial state.
            actions (dict): Dictionary of actions to execute for each state.
        """

        #Store reference to robot
        self.robot = robot

        # Initialize all FSMS
        """
        Functions in here will need to be binded with the C++ code via the communicator 
        to make things work
        """
        states = ['find far wall', 'turn towards wall', 'pos center', 'turn towards ramp']
        initial_state = 'find far wall'
        actions = { 'find far wall':self.find_far_wall,\
                    'turn towards wall':self.turn_robot,\
                    'pos center':self.move_to_center,\
                    'turn towards ramp': self.turn_robot }
        self.center_align_FSM = FiniteStateMachine(states, initial_state, actions)


        states = ['check image', 'move forward','array drive']
        initial_state = 'check image'
        actions = { 'check image':self.check_ramp_image,\
                    'move forward':self.move_forward,\
                    'array drive':self.array_drive}
        self.climb_ramp_FSM = FiniteStateMachine(states, initial_state, actions)


        #Initialize all FSM Managers (Bottom Down Approach)
        states = ['center align', 'climb ramp']
        initial_state = 'center align'
        children = { 'center align':self.center_align_FSM, #,\
                     'climb ramp':self.climb_ramp_FSM }
        self.entry_FSM = FiniteStateMachineManager(states, initial_state,children)


        states = ['enter', 'follow_arrows', 'exit']
        initial_state = 'enter'
        children = {'enter':self.entry_FSM }#,\
                   #'follow_arrows':self.follow_arrows,\
                   # 'exit':self.exit_region}
        self.D_GA_FSM = FiniteStateMachineManager(states, initial_state,children)




    def find_far_wall(self, fsm_instance):

        us_distances = self.robot.get_ultrasonic_distances()
        print(us_distances)
        if us_distances[0]-us_distances[-1]>5:
            #turn left
            fsm_instance.temp_kwargs = {'dir':'left'}
            print(fsm_instance.temp_kwargs)
            fsm_instance.transition_to_next()
        elif us_distances[0]-us_distances[-1]<-5:     
            #right
            fsm_instance.temp_kwargs = {'dir':'right'}
            print(fsm_instance.temp_kwargs)
            fsm_instance.transition_to_next()
        else:
            fsm_instance.tell_parent_switch()
            # fsm_instance has to tell the parent FSM to switch states
            pass
        

    def turn_robot(self, fsm_instance):
        direction = fsm_instance.temp_kwargs['dir']
        if direction=='left':
            print('Fellow telling me turn left', self.robot.getOrientation())
            self.robot.turn_left()
        elif direction == 'right':
            print('Fellow telling me turn right', self.robot.getOrientation())
            self.robot.turn_right()

    # climb_ramp_FSM funtions
    def check_ramp_image(self, fsm_instance):
        print("Trying to capture image")
        pass

    def move_forward():
        pass

    def array_drive():
        pass



    def move_to_center():
        pass



    def run(self):
        self.D_GA_FSM.execute_action()
        pass
