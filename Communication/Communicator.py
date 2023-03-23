import struct
from typing import Callable, List, Any, ByteString, DefaultDict, Dict, Iterable
from collections import defaultdict
from queue import Queue
import serial
from enum import Enum, auto


class Commands:
    TURN_LEFT = 1
    TURN_RIGHT = 2
    MOVE_FORWARD = 3
    STOP = 4
    TURN_THETA = 5
    GET_LINE_SENSOR = 6
    GET_ENCODERS = 7


class Communicator:
    def __init__(self, port: str, baud_rate, time_out):
        self.on_message_recieve: DefaultDict[int, List[Callable[[
            bytes], None]]] = defaultdict(lambda: [])
        self.message_queue: Queue[bytes] = Queue()
        self.serial = serial.Serial(
            port=port, baudrate=baud_rate, timeout=time_out)
        self.decoder_function_map: Dict[int,
                                        Callable[[bytes], Iterable[Any]]] = {}

        self.decoder_function_map[Commands.GET_ENCODERS] = self.encoder_data_decoder
        self.decoder_function_map[Commands.GET_LINE_SENSOR] = self.line_sensor_decoder

    def compile_message(self, message_index: int, data: List[Any]):
        header_index = struct.pack('c', message_index.to_bytes(1, 'big'))
        ret = b""
        for d in data:
            if(type(d) == float):
                ret += struct.pack('f', d)
            if(type(d) == int):
                ret += struct.pack('i', d)
        size = len(data)
        header_size = struct.pack('c', size.to_bytes(1, 'big'))
        return header_index+header_size+ret

    def register_function(self, message_index: int, call_back: Callable[[Iterable[Any]], None]):
        decoder = self.decoder_function_map[message_index]
        self.on_message_recieve[message_index].append(
            lambda x: call_back(decoder(x)))

    def communicate(self):
        while self.message_queue:
            message = self.message_queue.get()
            self.serial.write(message)
        while self.serial.in_waiting:
            index = int.from_bytes(self.serial.read(1), 'big')
            length = int.from_bytes(self.serial.read(1), 'big')
            data = self.serial.read(length)
            for func in self.on_message_recieve[index]:
                func(data)

    def compile_and_add_message(self, message_index: int, data: List[Any]):
        self.message_queue.put(self.compile_message(
            message_index, data
        ))

    def send_turn_left(self, speed: float):
        self.compile_and_add_message(Commands.TURN_LEFT, [speed])

    def send_turn_right(self, speed: float):
        self.compile_and_add_message(Commands.TURN_RIGHT, [speed])

    def send_move_forward(self, speed: float):
        self.compile_and_add_message(Commands.MOVE_FORWARD, [speed])

    def send_stop(self, speed: float):
        self.compile_and_add_message(Commands.STOP, [speed])

    def rotate_by_theta(self, angle: float):
        self.compile_and_add_message(Commands.TURN_THETA, [angle])

    def get_line_sensor_data(self):
        self.compile_and_add_message(Commands.GET_LINE_SENSOR, [])

    def get_encoder_data(self):
        self.compile_and_add_message(Commands.GET_ENCODERS, [])

    def encoder_data_decoder(self, data: bytes):
        return struct.unpack('ff', data)

    def line_sensor_decoder(self, data: bytes):
        return struct.unpack('f', data)
