
from MazeRunner import MazeRunner
from Grid import GridNode, Grid, NORTH, EAST, WEST, SOUTH, POS_DIRECTION_MAP, DIRECTIONS, OPPOSITE_DIRECTION
from typing import List, Tuple, Optional
import numpy as np


class MazeSolver:
    def __init__(self, mazeRunner: MazeRunner):
        self.mazeRunner = mazeRunner
        self.dfs_stack: List[Tuple[GridNode, Optional[int]]] = []
        self.principal_directions_found = 0
        self.principal_directions: List[int] = []
        self.corners: List[Tuple[int, int]] = []

    def initialize(self):
        self.dfs_stack.append((self.mazeRunner.grid.get_node(
            *self.mazeRunner.grid_position), None))
        self.dfs_stack[0][0].set_visited()

    def run_bfs(self):
        if(not self.dfs_stack):
            return True

        new_node, direction = self.dfs_stack[-1]
        current_grid_position = new_node.get_pos()
        current_node = self.mazeRunner.grid.get_node(*current_grid_position)
        connected_node = self.mazeRunner.grid.get_connected_nodes(
            *current_grid_position)

        for _, direction in connected_node:
            if(len(self.principal_directions) < 2 and direction
                not in self.principal_directions and direction
               not in [OPPOSITE_DIRECTION[x] for x in self.principal_directions]):
                self.principal_directions.append(direction)
                print(self.principal_directions)
                if(len(self.principal_directions) == 2):
                    print("Found Principal directions")
                    self.on_principal_direction_detect()
        for node, direction in connected_node:
            if(node.has_visited()):
                continue
            self.dfs_stack.append((node, direction))
            node.set_visited()
            self.mazeRunner.add_task_go_direction(direction)
            return False
        node, direction = self.dfs_stack.pop(-1)
        if(direction is None):
            return True

        self.mazeRunner.add_task_go_direction(OPPOSITE_DIRECTION[direction])
        return False

    def on_principal_direction_detect(self):
        STRIDE = self.mazeRunner.size-1
        principal_1, principal_2 = [
            np.array(POS_DIRECTION_MAP[x], dtype=int) for x in self.principal_directions]
        corner1 = np.array(self.mazeRunner.start_position,
                           dtype=int)+STRIDE*principal_1
        corner2 = np.array(self.mazeRunner.start_position,
                           dtype=int)+STRIDE*principal_2

        corner3 = np.array(self.mazeRunner.start_position,
                           dtype=int)+STRIDE*principal_2+STRIDE*principal_1
        self.corners = [tuple(corner)
                        for corner in (corner1, corner2, corner3)]
        for corner in self.corners:
            for direction in DIRECTIONS:
                node = self.mazeRunner.grid.get_node(*corner)
                self.mazeRunner.grid.set_wall_smart(node, direction)
                # self.mazeRunner.grid.get_node(*corner).set_wall(direction)
