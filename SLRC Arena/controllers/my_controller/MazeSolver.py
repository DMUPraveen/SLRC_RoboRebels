
from Motors import Motorcontrol
from DistanceSensors import DistanceSensors
from controller import Robot
from PID import PID
from Navigation import Alingment, LinearTraveller, Rotator
from Grid import Grid, GridNode, NORTH, EAST, SOUTH, WEST, LEFT, RIGHT, BACK, FRONT, target_dir_from_relaitve, POS_DIRECTION_MAP
from GraphicEngine import GraphicEngine, BLUE
from enum import Enum, auto
import math

ALIGNMENT_THRESHOLD = 0.01
LINEAR_TRAVEL_THRESHOLD = 0.01
ROTATION_THRESHOLD = 0.001

cell_size_in_meters = 0.36
forward_step = 0.38


class MazeRunner:
    def __init__(self, motorController: Motorcontrol, distanceSensors: DistanceSensors, linearTraveller: LinearTraveller,
                 rotator: Rotator, size: int):
        self.motorController = motorController
        self.distanceSensors = distanceSensors
        self.linearTraveller = linearTraveller
        self.alignment = Alingment(motorController, distanceSensors)
        self.rotator = rotator
        grid_size = size*2-2
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
        return True

    def turn_right(self):
        self.rotator.initialize(math.pi/2)
        while (self.rotator.run() > ROTATION_THRESHOLD):
            yield False
        self.pose_turn(RIGHT)
        return True

    def turn_left(self):
        self.rotator.initialize(-math.pi/2)
        while (self.rotator.run() > ROTATION_THRESHOLD):
            yield False
        self.pose_turn(LEFT)
        return True

    def turn_back(self):
        self.rotator.initialize(math.pi)
        while (self.rotator.run() > ROTATION_THRESHOLD):
            yield False
        self.pose_turn(BACK)
        return True

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

    def test_run(self):
        simple_align = self.simple_align()
        for _ in simple_align:
            yield False
        self.check_for_walls_and_build()
        for _ in range(2):
            go_forward = self.go_forward()
            for _ in go_forward:
                yield False
            alinger = self.align_with_any_wall()
            for _ in alinger:
                print("running alingment")
                yield False
            self.check_for_walls_and_build()
        turn_once = self.turn_left()
        for _ in turn_once:
            print("turning")
            yield False

        alinger = self.align_with_any_wall()
        for _ in alinger:
            print("running alingment")
            yield False
        for _ in range(1):
            go_forward = self.go_forward()
            for _ in go_forward:
                yield False
        alinger = self.align_with_any_wall()
        for _ in alinger:
            print("running alingment")
            yield False
        self.check_for_walls_and_build()
        while True:
            yield True

    def add_task()

    def run_execution_stack(self):
        while True:
            if(not self.execution_stack):
                yield True
            task = self.execution_stack.pop()
            for _ in task:
                yield False
