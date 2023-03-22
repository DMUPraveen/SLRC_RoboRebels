from Grid import NORTH, SOUTH, EAST, WEST, GridNode, DIRECTIONS
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)

CELL_SIZE = 20
WHITE = (255, 255, 255)

WALL_DELTAS = {
    NORTH: ((0, 0), (CELL_SIZE, 0)),
    SOUTH: ((0, CELL_SIZE), (CELL_SIZE, CELL_SIZE)),
    EAST: ((CELL_SIZE, 0), (CELL_SIZE, CELL_SIZE)),
    WEST: ((0, 0), (0, CELL_SIZE)),
}

OFFSET = (CELL_SIZE, CELL_SIZE)


def transform(a, b):
    return a[0]*CELL_SIZE+b[0]+OFFSET[0], a[1]*CELL_SIZE+b[1]+OFFSET[0]


class GraphicEngine:
    def __init__(self, width, height):
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.running = True

    def draw_cell(self, color, i, j):
        if(not self.running):
            return
        pygame.draw.rect(self.screen, color, (i*CELL_SIZE+OFFSET[0],
                         j*CELL_SIZE+OFFSET[1], CELL_SIZE, CELL_SIZE))

    def draw_node(self, node: GridNode):
        if(not self.running):
            return
        for direction in DIRECTIONS:
            if(node.has_wall(direction)):
                start, end = WALL_DELTAS[direction]
                y, x = node.get_pos()
                start = transform((x, y), start)
                end = transform((x, y), end)
                # print(start, end)
                pygame.draw.line(self.screen, BLACK, start, end)

    def clear(self):
        if(not self.running):
            return
        self.screen.fill(WHITE)

    def run(self):
        if(not self.running):
            return
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                self.running = False
                return
        pygame.display.update()
