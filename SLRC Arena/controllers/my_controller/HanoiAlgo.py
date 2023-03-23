
from Mazegoto import Mazegoto
from SuperStateMachineForCatchTheBox import SuperState
from PlacingOnTop import Hanoi

RED = 0
GREEN = 1
BLUE = 2

ATFER_PICKUP_FORWARD_THRESHOLD = 0.5


class HanoiRetrieve:
    def __init__(self, mazegoto: Mazegoto, superstate: SuperState, hanoi: Hanoi):
        self.mazegoto = mazegoto
        self.colors = [RED, GREEN, BLUE]
        self.initial_box_places = {
            RED: 0,
            GREEN: 1,
            BLUE: 2
        }
        self.superstate = superstate
        self.hanoi = hanoi

    def detect_color(self):
        return self.colors.pop()

    def pick_up_box(self):
        while not self.superstate.SuperStateMachine():
            print("Picking up box")
            yield

    def box_place_and_return_to_original_pos(self):
        while not self.hanoi.BuildHanoi(1):
            print("Placing Box")
            yield
        while not self.hanoi.pos.isHung():
            self.hanoi.arm.bringup()
            yield

    def retrieve_box(self, corner):
        partial_go = self.mazegoto.do_partial_go_from_current(corner)
        for _ in partial_go:
            yield
        color = self.detect_color()
        pick_up = self.pick_up_box()
        for _ in pick_up:
            yield
        go_forward_until_task = self.mazegoto.mazesolver.mazeRunner.go_forward_until_threshold_task(
            ATFER_PICKUP_FORWARD_THRESHOLD)
        for _ in go_forward_until_task:
            self.hanoi.arm.catchbox()
            yield
        self.mazegoto.mazesolver.mazeRunner.pose_advance()  # will travel one block forward
        yield
        # self.mazegoto.mazesolver.mazeRunner.add_vertical_centering_taks()
        # yield
        centering_task = self.mazegoto.mazesolver.mazeRunner.vertical_centering_task()
        for _ in centering_task:
            self.hanoi.arm.catchbox()
            yield
        target = self.initial_box_places[color]
        target_pos = self.mazegoto.stacks[target]
        partial_go = self.mazegoto.do_partial_go_from_current(
            target_pos, self.mazegoto.stacks)
        for _ in partial_go:
            self.hanoi.arm.catchbox()
            yield
        box_placer = self.box_place_and_return_to_original_pos()
        for _ in box_placer:
            yield
        return

    def retrieve_all_boxes(self):
        for corner in self.mazegoto.mazesolver.corners[::-1]:
            box_retriever = self.retrieve_box(corner)
            for _ in box_retriever:
                yield
