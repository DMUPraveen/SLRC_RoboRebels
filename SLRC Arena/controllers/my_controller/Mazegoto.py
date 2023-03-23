from MazeSolver import MazeSolver
from collections import deque
from Grid import GridNode
from typing import Deque, Tuple, Optional, List


class Mazegoto:
    def __init__(self, mazesolver: MazeSolver):
        self.mazesolver = mazesolver

    def find_path(self, start_pos, end_pos) -> Tuple[bool, List[int]]:

        start_node = self.mazesolver.mazeRunner.grid.get_node(*start_pos)
        end_node = self.mazesolver.mazeRunner.grid.get_node(*end_pos)

        target = None
        queue: Deque[GridNode] = deque()
        start_node.parent = None
        start_node.pre_dir = None
        queue.append(start_node)
        visited = [start_node]
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
