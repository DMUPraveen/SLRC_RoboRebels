from time import sleep, time
import serial
import json
import sys
import struct
BAUD_RATE = 9600


def main():

    COM_PORT = "COM4"
    if(len(sys.argv) > 1):
        COM_PORT = sys.argv[1]
        datafile = sys.argv[2]
    else:
        datafile = "data.json"

    data = {}
    with open(datafile, "r") as f:
        data = json.loads(f.read())

    instruction = 0
    length = 4*4
    header = struct.pack('c', instruction.to_bytes(1, 'big')) + \
        struct.pack('c', length.to_bytes(1, 'big'))
    data_list = [val for _, val in data.items()]
    output = header+b"".join(struct.pack('f', data) for data in data_list)
    print(output)

    arduino = serial.Serial(port=COM_PORT, baudrate=BAUD_RATE, timeout=5)
    sleep(2)
    arduino.write(output)
    arduino.flush()
    sleep(0.05)
    r = arduino.readline().decode('utf-8')
    print(r)


if __name__ == "__main__":
    main()
