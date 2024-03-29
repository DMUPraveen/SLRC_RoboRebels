
from Motors import Motorcontrol
from DistanceSensors import DistanceSensors
from controller import Robot
from PID import PID
from Navigation import Alingment, LinearTraveller, Rotator
from Grid import Grid, GridNode, NORTH, EAST, SOUTH, WEST, LEFT, RIGHT, BACK, FRONT, target_dir_from_relaitve, POS_DIRECTION_MAP, relative_dir
from GraphicEngine import GraphicEngine, BLUE
from enum import Enum, auto
import math
from types import GeneratorType
from ClassForPuttingBackTheBox import PutTHEDAMNBOX

ALIGNMENT_THRESHOLD = 0.001
LINEAR_TRAVEL_THRESHOLD = 0.01
ROTATION_THRESHOLD = 0.001

cell_size_in_meters = 0.36
forward_step = 0.38

CENTERING_THRESHOLD = 0.001
GO_FORWARD_UNTIL_THRESHOLD = 0.001


class MazeRunner:
    def __init__(self, motorController: Motorcontrol, distanceSensors: DistanceSensors, linearTraveller: LinearTraveller,
                 rotator: Rotator, size: int):
        self.motorController = motorController
        self.distanceSensors = distanceSensors
        self.linearTraveller = linearTraveller
        self.alignment = Alingment(motorController, distanceSensors)
        self.rotator = rotator
        grid_size = size*2-1
        self.grid_position = (size-1, size-1)
        self.position = self.grid_position[0] * \
            cell_size_in_meters, self.grid_position[1]*cell_size_in_meters
        self.grid = Grid(grid_size, grid_size)
        self.visited_stack = [
            [0 for _ in range(grid_size)]for _ in range(grid_size)]
        self.bfs_run = 0
        self.bfs_stack = []
        self.orientation = NORTH
        self.execution_stack = []
        self.size = size
        self.start_position = self.grid_position  # starting position of the robot

        self.always_run = []

    def estimate_position(self):
        if(self.distanceSensors.left_wall_present()):

            pass
        if(self.distanceSensors.right_wall_present()):
            pass
        if(self.distanceSensors.back_wall_present()):
            pass

    def pose_advance(self):
        delta = POS_DIRECTION_MAP[self.orientation]
        self.grid_position = (
            self.grid_position[0]+delta[0], self.grid_position[1]+delta[1])

    def pose_turn(self, rel_dir):
        td = target_dir_from_relaitve(self.orientation, rel_dir)
        self.orientation = td
        # print(self.orientation)

    def go_forward(self):
        self.linearTraveller.initialize(forward_step)
        while (self.linearTraveller.run() > LINEAR_TRAVEL_THRESHOLD):
            yield False
        self.pose_advance()
        self.motorController.pose_stop()
        return True

    def turn_right(self):
        self.rotator.initialize(math.pi/2)
        while (self.rotator.run() > ROTATION_THRESHOLD):
            yield False
        self.pose_turn(RIGHT)
        self.motorController.pose_stop()
        return True

    def turn_left(self):
        self.rotator.initialize(-math.pi/2)
        while (self.rotator.run() > ROTATION_THRESHOLD):
            yield False
        self.pose_turn(LEFT)
        self.motorController.pose_stop()
        return True

    def turn_back(self):
        self.rotator.initialize(math.pi)
        while (self.rotator.run() > ROTATION_THRESHOLD):
            yield False
        self.pose_turn(BACK)
        self.motorController.pose_stop()
        return True

    def turn_rel_dir(self, rel_dir):
        if(rel_dir == LEFT):
            return self.turn_left()
        if(rel_dir == RIGHT):
            return self.turn_right()
        if(rel_dir == BACK):
            return self.turn_back()

        return None

    def simple_align(self):
        while True:
            print("align left")
            error = self.alignment.align_to_left_wall()
            yield False
            if(error < ALIGNMENT_THRESHOLD):
                break
        while True:
            print("align back")
            error = self.alignment.align_to_back_wall()
            yield False
            if(error < ALIGNMENT_THRESHOLD):
                break
        while True:
            print("align left again")
            error = self.alignment.align_to_left_wall()
            yield False
            if(error < ALIGNMENT_THRESHOLD):
                break

    def align_with_any_wall(self):

        while self.distanceSensors.left_wall_present():
            # print("align left")
            error = self.alignment.align_to_left_wall()
            yield False
            if(error < ALIGNMENT_THRESHOLD):
                self.motorController.pose_stop()
                return

        while self.distanceSensors.back_wall_present():
            error = self.alignment.align_to_back_wall()
            yield False
            if(error < ALIGNMENT_THRESHOLD):
                self.motorController.pose_stop()
                return
        while self.distanceSensors.right_wall_present():
            error = self.alignment.align_to_right_wall()
            yield False
            if(error < ALIGNMENT_THRESHOLD):
                self.motorController.pose_stop()
                return

    def check_for_walls_and_build(self):
        '''
        checks if there are any walls in the current position and builds them
        '''
        print("Building walls")
        current_node = self.grid.get_node(*self.grid_position)
        if(self.distanceSensors.front_wall_present()):
            td = target_dir_from_relaitve(self.orientation, FRONT)
            current_node.set_wall(td)
        if(self.distanceSensors.left_wall_present()):
            td = target_dir_from_relaitve(self.orientation, LEFT)
            current_node.set_wall(td)
        if(self.distanceSensors.right_wall_present()):
            td = target_dir_from_relaitve(self.orientation, RIGHT)
            current_node.set_wall(td)
        if(self.distanceSensors.back_wall_present()):
            td = target_dir_from_relaitve(self.orientation, BACK)
            current_node.set_wall(td)

    def check_for_walls_and_build_smart(self):
        current_node = self.grid.get_node(*self.grid_position)
        if(self.distanceSensors.front_wall_present()):
            td = target_dir_from_relaitve(self.orientation, FRONT)
            self.grid.set_wall_smart(current_node, td)
        if(self.distanceSensors.left_wall_present()):
            td = target_dir_from_relaitve(self.orientation, LEFT)
            self.grid.set_wall_smart(current_node, td)
        if(self.distanceSensors.right_wall_present()):
            td = target_dir_from_relaitve(self.orientation, RIGHT)
            self.grid.set_wall_smart(current_node, td)
        if(self.distanceSensors.back_wall_present()):
            td = target_dir_from_relaitve(self.orientation, BACK)
            self.grid.set_wall_smart(current_node, td)

    def add_task_go_direction(self, direction: int):
        rel_dir = relative_dir(self.orientation, direction)
        turn_task = self.turn_rel_dir(rel_dir)
        if(turn_task is not None):
            self.execution_stack.append(turn_task)
        align_task = self.align_with_any_wall()
        self.execution_stack.append(align_task)
        forward_task = self.go_forward()
        self.execution_stack.append(forward_task)
        align_task = self.align_with_any_wall()
        self.execution_stack.append(align_task)
        self.execution_stack.append(self.check_for_walls_and_build_smart)

    def add_turn_to_direction(self, direction: int):
        rel_dir = relative_dir(self.orientation, direction)
        turn_task = self.turn_rel_dir(rel_dir)
        if(turn_task is not None):
            self.execution_stack.append(turn_task)
        align_task = self.align_with_any_wall()
        self.execution_stack.append(align_task)

    def run_execution_stack(self):
        while True:
            for func in self.always_run:
                func()
            if(not self.execution_stack):
                yield True
                continue

            task = self.execution_stack.pop(0)
            if type(task) == GeneratorType:
                for _ in task:
                    yield False
            else:
                task()
            yield False

    def add_task_build_wall(self):
        self.execution_stack.append(self.check_for_walls_and_build)

    def add_task_build_wall_smart(self):
        self.execution_stack.append(self.check_for_walls_and_build_smart)

    def add_task_aling(self):
        self.execution_stack.append(self.align_with_any_wall())

    def center_using_back_sensors_if_possible(self):

        while self.distanceSensors.back_wall_present():
            measurement = self.alignment.center_using_back_sensor()
            if(measurement < CENTERING_THRESHOLD):
                self.motorController.pose_stop()
                return True
            yield False

        print("Back wall is not present cannot center")
        return True

    def add_back_centering_task(self):
        self.add_task_aling()
        self.execution_stack.append(
            self.center_using_back_sensors_if_possible())

    def center_side(self):
        if not(self.distanceSensors.left_wall_present() or self.distanceSensors.right_wall_present()):
            print("Side wall not present centering not possible")
            return True
        if(self.distanceSensors.left_wall_present()):
            turning = self.turn_right()
        else:
            turning = self.turn_left()
        for val in turning:
            yield val
        align = self.align_with_any_wall()
        for val in align:
            yield val
        centering = self.center_using_back_sensors_if_possible()
        for val in centering:
            yield val
        return True

    def vertical_centering_task(self):
        if not(self.distanceSensors.back_wall_present() or self.distanceSensors.front_wall_present()):
            print("Vertical Alingment not possible")
            return True
        if not(self.distanceSensors.back_wall_present()):
            turning = self.turn_back()
            for val in turning:
                yield val
        align = self.align_with_any_wall()
        for val in align:
            yield val
        centering = self.center_using_back_sensors_if_possible()
        for val in centering:
            yield val
        return True

    def add_side_centering_task(self):
        self.add_task_aling()
        self.execution_stack.append(self.center_side())

    def add_vertical_centering_taks(self):
        self.add_task_aling()
        self.execution_stack.append(self.vertical_centering_task())

    def add_total_centering_taks(self):
        self.add_vertical_centering_taks()
        self.add_side_centering_task()

    def go_forward_until_threshold_task(self, threshold: float):
        '''
        Use with caution Pose is not updated 
        threshold is in distance sensor units [0,1]
        '''
        while self.alignment.go_forward_unit_threshold(threshold) > GO_FORWARD_UNTIL_THRESHOLD:
            yield False
        return True
