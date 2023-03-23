from MazeSolver import MazeSolver
from collections import deque
from Grid import GridNode, POS_DIRECTION_MAP, DIRECTIONS
from typing import Deque, Tuple, Optional, List
import numpy as np


class Mazegoto:
    def __init__(self, mazesolver: MazeSolver):
        self.mazesolver = mazesolver
        self.stacks: List[Tuple[int, int]] = []

    def find_places(self):
        STRIDE = 2
        principal_1, principal_2 = [
            np.array(POS_DIRECTION_MAP[x], dtype=int) for x in self.mazesolver.principal_directions]
        start = np.array(self.mazesolver.mazeRunner.start_position, dtype=int)
        first = start+STRIDE*principal_1+STRIDE*principal_2
        new_strid = principal_1
        for i in range(3):
            for j in range(3):
                if(i == 1 and j == 1):
                    continue
                npos = first+principal_1*i+principal_2*j
                node = self.mazesolver.mazeRunner.grid.get_node(*npos)
                free = True
                for direction in DIRECTIONS:
                    if(node.has_wall(direction)):
                        free = False
                        break
                if(not free):
                    continue
                if(j < i):
                    new_strid = principal_2
                else:
                    new_strid = principal_1
                break
        for k in range(3):
            self.stacks.append(tuple(first+new_strid*k))

    def find_path(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], black_listed: Optional[List[Tuple[int, int]]] = None) -> Tuple[bool, List[int]]:
        '''
        black_listed nodes only apply to intermediate nodes it will still go to a end_pos even if
        the corresponding node is blacklisted 
        '''

        start_node = self.mazesolver.mazeRunner.grid.get_node(*start_pos)
        end_node = self.mazesolver.mazeRunner.grid.get_node(*end_pos)

        target = None
        queue: Deque[GridNode] = deque()
        start_node.parent = None
        start_node.pre_dir = None
        queue.append(start_node)

        visited = [start_node]
        if(black_listed is not None):
            black_listed_nodes = [
                self.mazesolver.mazeRunner.grid.get_node(*node) for node in black_listed]
            if(end_node in black_listed_nodes):
                black_listed_nodes.remove(end_node)
            if(start_node in black_listed_nodes):
                black_listed_nodes.remove(start_node)
            visited.extend(black_listed_nodes)
        while queue:
            cn = queue.popleft()  # current node
            c_node = cn
            if(c_node is end_node):
                target = cn
                break
            connected_nodes = self.mazesolver.mazeRunner.grid.get_connected_nodes(
                *c_node.get_pos())
            for node, direction in connected_nodes:
                if(node in visited):
                    continue
                visited.append(node)
                node.parent = c_node
                node.pre_dir = direction
                queue.append(node)

        if(target is None):
            return (False, [])

        directions = []

        node = target

        while node.pre_dir is not None:
            directions.append(node.pre_dir)
            node = node.parent
            assert(node is not None)

        return (True, directions[::-1])

    def do_go_path(self, directions: List[int]):
        self.mazesolver.mazeRunner.add_total_centering_taks()
        yield
        for direction in directions:
            self.mazesolver.mazeRunner.add_task_go_direction(direction)
            yield

    def do_partial_go_from_current(self, end_pos: Tuple[int, int], black_listed_node: Optional[List[Tuple[int, int]]] = None):
        '''
        goes upto the last cell but not on to it 
        '''
        self.mazesolver.mazeRunner.add_total_centering_taks()
        yield
        path_found, directions = self.find_path(
            self.mazesolver.mazeRunner.grid_position, end_pos, black_listed_node)
        for direction in directions[:-1]:
            self.mazesolver.mazeRunner.add_task_go_direction(direction)
            yield
        self.mazesolver.mazeRunner.add_turn_to_direction(directions[-1])
