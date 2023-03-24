from Mazegoto import Mazegoto
from MazeSolver import MazeSolver
from Motors import Motorcontrol
from HanoiAlgo import HanoiRetrieve
from SuperStateMachineForCatchTheBox import SuperState
from PlacingOnTop import Hanoi
from Grabber import GrabBox


def main_control_code(mazesolver: MazeSolver, mazegoto: Mazegoto,
                      motorcontrol: Motorcontrol, superstate: SuperState, hanoi: Hanoi, grabbox: GrabBox):
    while not mazesolver.run_bfs():
        yield
    mazegoto.find_places()
    retriever = HanoiRetrieve(mazegoto, superstate, hanoi, grabbox)
    retriever_task = retriever.retrieve_all_boxes()
    for _ in retriever_task:
        yield
    hanoi_make = retriever.make_tower()
    for _ in hanoi_make:
        yield
    yield
    while True:
        print("finished")
        yield
