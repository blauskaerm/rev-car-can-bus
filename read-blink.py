import socket
import sys
import struct

interface = "vcan0"
can_socket = socket.socket(socket.PF_CAN,
                           socket.SOCK_RAW,
                           socket.CAN_RAW)

try:
    can_socket.bind((interface, ))
except OSError:
    print("Could not bind to CAN interface '%s'\n" % interface, flush=True)


CAN_DATA_FORMAT = "<IB3x8s"
CAN_BLINK_ID = 0x188
CAN_BLINK_LEFT = 0x01
CAN_BLINK_RIGHT = 0x02

while True:

    can_pkt = can_socket.recv(16)
    can_id, can_msg_length, can_data = struct.unpack(CAN_DATA_FORMAT,
                                                     can_pkt)
    can_id &= socket.CAN_EFF_MASK
    if can_id == CAN_BLINK_ID:

        can_data = can_data[:can_msg_length]
        can_blink_position = can_data[0]

        if can_blink_position == CAN_BLINK_LEFT:
            print("Blink left")
        elif can_blink_position == CAN_BLINK_RIGHT:
            print("Blink right")
