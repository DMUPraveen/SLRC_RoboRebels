from Communicator import Communicator, Commands
from time import sleep


def main():
    BAUD_RATE = 9600
    COM_PORT = "COM4"
    com = Communicator(COM_PORT, BAUD_RATE, 0.5)
    com.register_function(Commands.GET_ENCODERS, print)
    com.register_function(Commands.GET_LINE_SENSOR, print)
    com.get_encoder_data()
    com.get_line_sensor_data()
    sleep(1)
    while True:
        com.communicate()
