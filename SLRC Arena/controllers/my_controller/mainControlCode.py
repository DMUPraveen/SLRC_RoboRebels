from Mazegoto import Mazegoto
from MazeSolver import MazeSolver
from Motors import Motorcontrol


def main_control_code(mazesolver: MazeSolver, mazegoto: Mazegoto, motorcontrol: Motorcontrol):
    while not mazesolver.run_bfs():
        yield
    mazegoto.find_places()
    do_partial_go = mazegoto.do_partial_go_from_current(
        mazegoto.stacks[2], mazegoto.stacks)
    for _ in do_partial_go:
        yield
    while True:
        print("finished")
        yield
