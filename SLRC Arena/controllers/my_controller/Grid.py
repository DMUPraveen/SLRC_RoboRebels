from typing import Tuple, List
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


LEFT = 3
RIGHT = 1
FRONT = 0
BACK = 2


def target_dir_from_relaitve(current_dir, relative_dir):
    return (current_dir+relative_dir) % 4


def relative_dir(current_dir, final_dir):
    return (final_dir-current_dir) % 4


POS_DIRECTION_MAP = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    EAST: (0, 1),
    WEST: (0, -1)
}

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]


class GridNode:
    def __init__(self, row: int, column: int):
        self.wall_states = [False]*4
        self.row: int = row
        self.column: int = column
        self.visited = 0

    def set_wall(self, direction):
        self.wall_states[direction] = True

    def set_visited(self):
        self.visited = 1

    def has_visited(self):
        return self.visited

    def has_wall(self, direction):
        return self.wall_states[direction]

    def get_connected_directions(self):
        connected_directions = []
        for direction in DIRECTIONS:
            if self.has_wall(direction):
                continue
            connected_directions.append(direction)
        return connected_directions

    def get_pos(self):
        return (self.row, self.column)


class Grid:
    def __init__(self, rows, columns) -> None:
        self.grid = [[GridNode(row, column) for column in range(columns)]
                     for row in range(rows)]
        self.put_walls()

    def get_node(self, row: int, column: int):
        return self.grid[row][column]

    def get_connected_nodes(self, row, column):
        node = self.get_node(row, column)
        connected_directions = node.get_connected_directions()
        connected_nodes: List[Tuple[GridNode, int]] = []
        for direction in connected_directions:
            dr, dc = POS_DIRECTION_MAP[direction]
            new_row, new_column = (row+dr, column+dc)
            new_node = self.get_node(new_row, new_column)
            connected_nodes.append(
                (new_node, direction)
            )

        return connected_nodes

    def put_walls(self):
        for node in self.grid[0]:
            node.set_wall(NORTH)
        for node in self.grid[-1]:
            node.set_wall(SOUTH)

        for node in [self.grid[i][0] for i in range(len(self.grid))]:
            node.set_wall(WEST)

        for node in [self.grid[i][-1] for i in range(len(self.grid))]:
            node.set_wall(EAST)


ABS_DIRECTIONS = {
    NORTH: "NORTH",
    SOUTH: "SOUTH",
    EAST: "EAST",
    WEST: "WEST"
}
REL_DIRECTIONS = {
    FRONT: "FRONT",
    BACK: "BACK",
    LEFT: "LEFT",
    RIGHT: "RIGHT"
}


def str_abs_dirs(direction):
    return ABS_DIRECTIONS[direction]


def str_rel_dirs(direction):
    return REL_DIRECTIONS[direction]
