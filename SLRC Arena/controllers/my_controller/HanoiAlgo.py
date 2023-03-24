
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

color_str_map = {
    RED: "red",
    GREEN: "green",
    BLUE: "blue"
}


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
        col = self.superstate.cam.ColorDetect()
        if(col == 'green'):
            return GREEN
        if(col == 'red'):
            return RED

        return BLUE

    def pick_up_box(self):
        for _ in range(WAIT_TIME//2):
            self.grabbox.downmotor()
            print("Waiting and Releasing")
            yield
        self.superstate.state = 0
        self.superstate.boxdetector.state = 0
        self.superstate.superarm.state = 0
        while not self.superstate.SuperStateMachine():
            print("Picking up box")
            yield

    def box_place_and_return_to_original_pos(self, color, place_height=1):
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

        if(color != BLUE):
            for _ in range(WAIT_TIME//2):
                self.hanoi.arm.putinback(-11, -0.8, -0.85,
                                         0, -1.47)  # """Put in back"""
                print("Waiting and Releasing")
                yield

        if(color != BLUE):
            for _ in range(WAIT_TIME//2):
                self.grabbox.upmotor()
                yield

        for _ in range(WAIT_TIME//2):
            self.hanoi.arm.catchbox()
            print("Waiting and Releasing")
            yield

        while not self.hanoi.BuildHanoi(place_height):
            print("Placing Box")
            yield
        for _ in range(WAIT_TIME):
            print("Waiting")
            yield

        for _ in range(WAIT_TIME//2):
            self.hanoi.arm.releasefingers()  # Releases the speed
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

    def get_box_and_put(self, start, end):
        partial_go = self.mazegoto.do_partial_go_from_current(start)
        for _ in partial_go:
            yield
        yield
        color = self.detect_color()
        pick_up = self.pick_up_box()
        for _ in pick_up:
            yield
        for _ in range(WAIT_TIME//2):
            print("Waiting")
            # self.grabbox.downmotor()
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
        partial_go = self.mazegoto.do_partial_go_from_current(
            end, self.mazegoto.stacks)
        for _ in partial_go:
            yield
        yield
        self.mazegoto.mazesolver.mazeRunner.motorController.pose_stop()
        box_placer = self.box_place_and_return_to_original_pos(color)
        for _ in box_placer:
            yield
        return

    def retrieve_box(self, corner):
        partial_go = self.mazegoto.do_partial_go_from_current(corner)
        for _ in partial_go:
            yield
        yield
        color = self.detect_color()
        pick_up = self.pick_up_box()
        for _ in pick_up:
            yield
        for _ in range(WAIT_TIME//2):
            print("Waiting")
            print(color_str_map[color])
            # self.grabbox.downmotor()
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
        box_placer = self.box_place_and_return_to_original_pos(color)
        for _ in box_placer:
            yield
        return

    def retrieve_all_boxes(self):
        for corner in self.mazegoto.mazesolver.corners[::-1]:
            box_retriever = self.retrieve_box(corner)
            for _ in box_retriever:
                yield

    def make_tower(self):
        pass
