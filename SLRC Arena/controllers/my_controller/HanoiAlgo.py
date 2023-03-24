
from Mazegoto import Mazegoto
from SuperStateMachineForCatchTheBox import SuperState
from PlacingOnTop import Hanoi
from Navigation import LinearTraveller
from PID import PID
from Grabber import GrabBox

RED = 0
GREEN = 1
BLUE = 2

ATFER_PICKUP_FORWARD_THRESHOLD = 0.5
WAIT_TIME = 10000//32
PLACE_DISTANCE = 0.36
PLACE_DISTANCE_THRESHOLD = 0.001


class HanoiRetrieve:
    def __init__(self, mazegoto: Mazegoto, superstate: SuperState, hanoi: Hanoi, grabbox: GrabBox):
        self.mazegoto = mazegoto
        self.colors = [RED, GREEN, BLUE]
        self.initial_box_places = {
            RED: 0,
            GREEN: 1,
            BLUE: 2
        }
        self.superstate = superstate
        self.hanoi = hanoi
        self.grabbox = grabbox

    def detect_color(self):
        return self.colors.pop()

    def pick_up_box(self):
        self.superstate.state = 0
        self.superstate.boxdetector.state = 0
        self.superstate.superarm.state = 0
        while not self.superstate.SuperStateMachine():
            print("Picking up box")
            yield

    def box_place_and_return_to_original_pos(self):
        self.mazegoto.mazesolver.mazeRunner.linearTraveller.initialize(
            PLACE_DISTANCE/2)
        while self.mazegoto.mazesolver.mazeRunner.linearTraveller.run() > PLACE_DISTANCE_THRESHOLD:
            print("Doing distance")
            yield
        self.mazegoto.mazesolver.mazeRunner.motorController.pose_stop()

        for _ in range(WAIT_TIME//2):
            self.grabbox.release()
            print("Waiting and Releasing")
            yield

        for _ in range(WAIT_TIME//2):
            self.hanoi.arm.putinback(-11, -0.8, -0.85,
                                     0, -1.47)  # """Put in back"""
            print("Waiting and Releasing")
            yield

        for _ in range(WAIT_TIME//2):
            self.grabbox.upmotor()
            yield
        for _ in range(WAIT_TIME//2):
            self.hanoi.arm.catchbox()
            print("Waiting and Releasing")
            yield

        while not self.hanoi.BuildHanoi(1):
            print("Placing Box")
            yield
        for _ in range(WAIT_TIME):
            print("Waiting")
            yield

        for _ in range(WAIT_TIME//2):
            self.hanoi.arm.releasefingers()
            print("Waiting and Releasing")
            yield

        self.mazegoto.mazesolver.mazeRunner.linearTraveller.initialize(
            -PLACE_DISTANCE/2)
        while self.mazegoto.mazesolver.mazeRunner.linearTraveller.run() > PLACE_DISTANCE_THRESHOLD:
            yield
        self.mazegoto.mazesolver.mazeRunner.motorController.pose_stop()
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
        for _ in range(WAIT_TIME//2):
            print("Waiting")
            self.grabbox.downmotor()
            self.grabbox.release()
            yield
        self.hanoi.arm.releasefingers()
        yield
        for _ in range(WAIT_TIME//2):
            print("Waiting")
            yield
        self.grabbox.grab()
        yield
        for _ in range(WAIT_TIME//2):
            print("Waiting")
            yield
        self.grabbox.stop()
        yield
        

        go_forward_until_task = self.mazegoto.mazesolver.mazeRunner.go_forward_until_threshold_task(
            ATFER_PICKUP_FORWARD_THRESHOLD)
        for _ in go_forward_until_task:
            # self.hanoi.arm.catchbox()
            yield
        self.mazegoto.mazesolver.mazeRunner.pose_advance()  # will travel one block forward
        yield
        # self.mazegoto.mazesolver.mazeRunner.add_vertical_centering_taks()
        # yield
        centering_task = self.mazegoto.mazesolver.mazeRunner.vertical_centering_task()
        for _ in centering_task:
            yield
        target = self.initial_box_places[color]
        target_pos = self.mazegoto.stacks[target]
        partial_go = self.mazegoto.do_partial_go_from_current(
            target_pos, self.mazegoto.stacks)
        for _ in partial_go:
            yield
        yield
        self.mazegoto.mazesolver.mazeRunner.motorController.pose_stop()
        box_placer = self.box_place_and_return_to_original_pos()
        for _ in box_placer:
            yield
        return

    def retrieve_all_boxes(self):
        for corner in self.mazegoto.mazesolver.corners[::-1]:
            box_retriever = self.retrieve_box(corner)
            for _ in box_retriever:
                yield
