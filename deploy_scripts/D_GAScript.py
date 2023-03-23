from finite_state_machine import FiniteStateMachine, FiniteStateMachineManager
import feature_extractor
import preprocessor
from main import get_bearing, get_closest_blob_coord
import cv2
import numpy as np
import math

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
        self.arrow_recog_lastRunTime = 0

        # Initialize all FSMS
        """
        Functions in here will need to be binded with the C++ code via the communicator 
        to make things work
        """
        states = ['find far wall', 'turn towards wall', 'pos center', 'turn towards ramp']
        initial_state = 'find far wall'
        actions = { 'find far wall':self.find_far_wall,\
                    'turn towards wall':self.turn_robot,\
                    'pos center':self.pos_to_center,\
                    'turn towards ramp': self.turn_robot }
        self.center_align_FSM = FiniteStateMachine(states, initial_state, actions)


        states = ['check image', 'move forward','array drive']
        initial_state = 'check image'
        actions = { 'check image':self.check_ramp_image,\
                    'move forward':self.move_stght_till_array_trig,\
                    'array drive':self.array_drive}
        self.climb_ramp_FSM = FiniteStateMachine(states, initial_state, actions)


        states = ['track arrow', 'blind drive', 'array drive', 'is_exit']
        initial_state = 'track first arrow'
        actions = { 'track first arrow':self.cap_first_arrow,\
                    'track next arrow':self.cap_next_arrow,\
                    'blind drive': self.blind_find_arrow,\
                    'array drive':self.array_align_arrow,\
                    'is_exit': self.check_exit_found }
        self.follow_arrows = FiniteStateMachine(states, initial_state,actions)


        states = ['color sensor valid', 'array drive', 'park']
        initial_state = 'color sensor valid'
        actions = { 'color sensor valid':self.empty_todo, 
                    'array drive':self.empty_todo,
                    'park': self.empty_todo }
        self.exit_region = FiniteStateMachine(states, initial_state,actions)


        #Initialize all FSM Managers (Bottom Down Approach)
        states = ['center align', 'climb ramp']
        initial_state = 'center align'
        children = { 'center align':self.center_align_FSM, #,\
                     'climb ramp':self.climb_ramp_FSM }
        self.entry_FSM = FiniteStateMachineManager(states, initial_state,children)

        states = ['enter', 'follow_arrows', 'exit']
        initial_state = 'follow_arrows'
        children = {'enter':self.entry_FSM ,\
                   'follow_arrows' : self.follow_arrows,\
                   'exit':self.exit_region }
        self.D_GA_FSM = FiniteStateMachineManager(states, initial_state,children)

    def empty_todo(self, fsm_instance):
        print('Reached Empty Function. Implement me at.')
        print("FSM :\t", fsm_instance.current_state)


    def find_far_wall(self, fsm_instance):

        us_distances = self.robot.get_ultrasonic_distances()
        centerOffset = us_distances[0]-us_distances[-1]
        print("CO:",centerOffset)
        if centerOffset>5:
            #turn left
            fsm_instance.dump_kwargs()
            fsm_instance.temp_kwargs['dir'] = 'left'

            targets = self.robot.get90_enc_targets(left = True)
            fsm_instance.temp_kwargs['targetEnc'] =targets
            fsm_instance.temp_kwargs['forward target'] = 0.5*(us_distances[0]+us_distances[-1])
            
            fsm_instance.transition_to_next()
        elif centerOffset<-5:     
            #right
            fsm_instance.dump_kwargs()
            fsm_instance.temp_kwargs['dir'] = 'right'
            targets = self.robot.get90_enc_targets(left = False)
            fsm_instance.temp_kwargs['targetEnc'] =targets
            fsm_instance.temp_kwargs['forward target'] = 0.5*(us_distances[0]+us_distances[-1])

            fsm_instance.transition_to_next()
        else:
            # fsm_instance has to tell the parent FSM to switch states
            fsm_instance.tell_parent_switch()
        

    def turn_robot(self, fsm_instance):
        error_threshold_turning = 0.5
        direction = fsm_instance.temp_kwargs['dir']
        # Error is the difference between current encoder reading and target reading
        # continue turning till th error become zero
        if direction=='left':
            self.robot.turn_left()
        elif direction == 'right':
            self.robot.turn_right()

        error = np.abs(self.robot.get_encoder_val()-fsm_instance.temp_kwargs['targetEnc'])
        error = np.sum(error)
        print(self.robot.get_encoder_val(), '\t', fsm_instance.temp_kwargs['targetEnc'], end='')
        print('Error :\t', error)
        if error < error_threshold_turning:
            self.robot.stop()
            fsm_instance.transition_to_next() 


    # climb_ramp_FSM funtions
    def check_ramp_image(self, fsm_instance):
        # find the two long vertical lines
        # than drive forward. when all the lines sensors dont detect 
        # white start following the line.

        blurRate = 25
        b    = preprocessor.blur(self.robot.get_camera_feed(), blurRate)
        otsu = preprocessor.applyOtsu(b)
        edge = preprocessor.canny(otsu)
        

        cp_edge = np.copy(edge)
        edge_perimeters = len(np.where(cp_edge>0)[0])
        th = 0.025*edge_perimeters
        mplin = 0.03*edge_perimeters
        mxgap = 0.04*edge_perimeters
        pot_vertical_lines, _ = feature_extractor.openCV_houghlines(cp_edge, int_thresh=th, minPoint_line=mplin, maxLine_gap=mxgap) 

        print('Got %i lines'%(len(pot_vertical_lines)))
        filter_lines = feature_extractor.rampVerticalHelper(pot_vertical_lines, angleThreshold=25)
        print('Finally have %i lines'%(len(filter_lines)))

        # Draw the five lines
        filterCopy = np.copy(edge)
        filterCopy = cv2.cvtColor(filterCopy, cv2.COLOR_GRAY2BGR)
        for l in filter_lines:
            cv2.line(filterCopy, (l.vertex1[0], 480-l.vertex1[1]), (l.vertex2[0], 480-l.vertex2[1]), (255,0,255), 3, cv2.LINE_AA)


        longestPair = feature_extractor.find_closest_and_longest(filter_lines)[0]
        center = np.array(longestPair[0].get_midpoint()+longestPair[1].get_midpoint())/2

        finalTake = np.copy(edge)
        finalTake = cv2.cvtColor(finalTake, cv2.COLOR_GRAY2BGR)
        for l in longestPair:
            cv2.line(finalTake, (l.vertex1[0], 480-l.vertex1[1]), (l.vertex2[0], 480-l.vertex2[1]), (0,0,255), 3, cv2.LINE_AA)

        errorX = center[0]-(b.shape[1]/2)
        #give positive offset to right of errorX>0
        #give positive offset to left if errorX <0

        # cv2.imshow('Canny', edge)
        # cv2.imshow('Lines', cp_edge)
        # cv2.imshow('Looking at', filterCopy)
        # cv2.imshow('My line is', finalTake)
        # cv2.waitKey(self.robot.timeStep)

        offset = 0.01*errorX
        self.robot.set_speed(offset, -offset) 
        print(offset, center, b.shape[1])
        if np.abs(errorX)<2:
            self.robot.stop()
            fsm_instance.transition_to_next()

    def pos_to_center(self, fsm_instance):
        self.robot.move_forward()

        #Transition Conditions
        forward_distance = self.robot.get_ultrasonic_distances()[1]
        error = np.abs(forward_distance-fsm_instance.temp_kwargs['forward target'])
        

        if np.abs(error)<70:
            #turn the robot back to the forward direction
            if fsm_instance.temp_kwargs['dir']=='right':
                #  Turn Right
                fsm_instance.temp_kwargs['dir'] = 'left'
                print(self.robot.get_encoder_val())
                targets = self.robot.get90_enc_targets(left = True)
                print(targets)
                fsm_instance.temp_kwargs['targetEnc'] =targets
            else:
                # Turn Left
                fsm_instance.temp_kwargs['dir'] = 'right'
                print(self.robot.get_encoder_val())
                targets = self.robot.get90_enc_targets(left = False)
                print(targets)
                fsm_instance.temp_kwargs['targetEnc'] =targets
            fsm_instance.transition_to_next()

                
    def move_stght_till_array_trig(self, fsm_instance):
        self.robot.move_forward()
        # check if the ir array has detected a line
        lineSensors = self.robot.get_line_sensor_val()
        darkCount = np.sum(lineSensors<500)
        if darkCount >3:
            self.robot.stop()
            fsm_instance.dump_kwargs()
            fsm_instance.temp_kwargs['ramp_start_dis'] = self.robot.get_encoder_val()
            fsm_instance.transition_to_next()
        # if the line is detected activate pid controller until all the ir sensors go white

        # 
        pass

    def array_drive(self, fsm_instance):
        # get encoder values 
        # give linear velocity
        # caluculate offset 
        # apply offset 
        # make motors turn 

        # Look for exit condition
        linear_speed = 2
        arr=self.robot.get_line_sensor_val()
        error= 1*arr[0]+0.5*arr[1]+0.25*arr[2]-0.25*arr[3]-0.5**arr[4]-1*arr[5]
        gamma= 0.0005
        lspeed=linear_speed-error*gamma
        rspeed=linear_speed+error*gamma
        self.robot.set_speed(lspeed,rspeed)

        whiteCount = np.sum(arr>500)
        climbedRamp = np.any((self.robot.get_encoder_val()-fsm_instance.temp_kwargs['ramp_start_dis'])>7)
        if whiteCount>4 and climbedRamp:
            self.robot.stop()
            fsm_instance.transition_to_next()
        # if error<=0.3 and arr[2]<=275 and arr[3]<=275:
        #     return True
    
    # ------------- follow_arrows actions ------------- #

    def cap_first_arrow(self, fsm_instance):
    # TODO : If arrow is not visible just as you enter rotate to the left to find the first arrow
    # TODO : continious tractking of arrow objects

        # To prevent webots crashing run function every 3 milli seconds
        if np.abs(self.arrow_recog_lastRunTime-self.robot.getTime())>2.5:
            self.arrow_recog_lastRunTime = self.robot.getTime()
            img = self.robot.get_camera_feed()

            error_path = "E:\\DEEE\\4th SEM\\SLRC 23\\root\\error_images\\errorImg2.jpg"
            cv2.imwrite(error_path, img)
            #print('Waiting for arrow data', end='\t')

            arrow_data = get_closest_blob_coord(img)

            # move towards the arrow 
            if arrow_data[0]:
                # align with the arrow centeroid
                linear_spped = 1
                errorX = arrow_data[1].get_center()[0] - self.robot.cam.getWidth()/2
                offset = 0.00075*errorX

                if abs(errorX)>10:
                    left =  +offset 
                    right = -offset
                    self.robot.set_speed(left, right)
                else:
                    left =  linear_spped+offset 
                    right = linear_spped-offset
                    self.robot.set_speed(left, right)                   

                # try to get the bearing and store in a buffer
                if arrow_data[2]!=-1:
                    if not(arrow_data[2]): # the image wasn't clipped
                        #print('Stored arrow center..', end='\t')
                        # try to get the bearing and store in a FILO buffer
                        print('Trying to get bearing \t ', end='')
                        error_path = "E:\\DEEE\\4th SEM\\SLRC 23\\root\\error_images\\errorImg3.jpg"
                        cv2.imwrite(error_path, img)
                        
                        # confidence, heading_towards, largestBlob.get_center()
                        confi, bearingAngle = get_bearing(img, imgVerbose=True)
                        print(confi, bearingAngle, 'Done')
                        try:
                            fsm_instance.temp_kwargs['bearing buffer'].append(bearingAngle)
                        except KeyError:
                            fsm_instance.temp_kwargs['bearing buffer'] = [bearingAngle]
                    else:
                        self.robot.stop()
                        fsm_instance.transition_to('blind drive')



    def blind_find_arrow(self, fsm_instance):
        
        linear_speed = 2
        arr=self.robot.get_line_sensor_val()


        whiteCount = np.sum(arr>500)
        self.robot.move_forward()

        if whiteCount>1:
            self.robot.stop()
            fsm_instance.transition_to('array drive')


    def decode_arrow(self, fsm_instance):        
        # sure and shot figure which way the arrow is pointing
        #self.track_blob(fsm_instance)
        pass


    def cap_next_arrow(self, fsm_instance):
        pass


    def array_align_arrow(self, fsm_instance):
        
        # Look for exit condition
        linear_speed = 0.5
        arr=self.robot.get_line_sensor_val()
        error= 1*arr[0]+0.5*arr[1]+0.25*arr[2]-0.25*arr[3]-0.5**arr[4]-1*arr[5]
        gamma= 0.0025
        lspeed=linear_speed-error*gamma
        rspeed=linear_speed+error*gamma
        self.robot.set_speed(lspeed,rspeed)

        blackCount = np.sum(arr<500)
        print(blackCount)
        if blackCount==6:
            self.robot.stop()
            
            #fsm_instance.transition_to('turn_to_direction')
            


    def to_next_arrow(self, fsm_instance):
        pass


    def check_exit_found(self, fsm_instance):
        pass

    
    def run(self):
        #self.array_drive()
        self.D_GA_FSM.execute_action()
        #print(self.robot.get_ultrasonic_distances())
        # if self.array_drive():
        #     self.robot.move_forward()
        # self.move_to_center()

    # ------------- exit_ region actions ------------- #
      

    # def stateMachine(self):
    #     if self.state==0:
    #         self.center_align_FSM
    #         self.state=1

    #     if self.state==1:
    #         self.climb_ramp_FSM
    #         self.state=2

    #     if self.state==2:
    #         self.entry_FSM
    #         self.state=3

    #     if self.state==3:
    #         self.D_GA_FSM
    #         self.state=4


        

