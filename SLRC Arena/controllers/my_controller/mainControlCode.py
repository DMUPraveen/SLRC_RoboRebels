from Mazegoto import Mazegoto
from MazeSolver import MazeSolver
from Motors import Motorcontrol
from HanoiAlgo import HanoiRetrieve


def main_control_code(mazesolver: MazeSolver, mazegoto: Mazegoto, motorcontrol: Motorcontrol):
    while not mazesolver.run_bfs():
        yield
    mazegoto.find_places()
    retriever = HanoiRetrieve(mazegoto)
    retriever_task = retriever.retrieve_all_boxes()
    for _ in retriever_task:
        yield
    while True:
        print("finished")
        yield
