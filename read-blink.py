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

CAN_VELOCITY_ID = 0x244

CAN_BLINK_ID = 0x188
CAN_BLINK_LEFT = 0x01
CAN_BLINK_RIGHT = 0x02

v_print_guard = 0
while True:

    can_pkt = can_socket.recv(16)
    can_id, can_msg_length, can_data = struct.unpack(CAN_DATA_FORMAT,
                                                     can_pkt)
    can_id &= socket.CAN_EFF_MASK
    can_data = can_data[:can_msg_length]


    if can_id == CAN_BLINK_ID:

        can_blink_position = can_data[0]

        if can_blink_position == CAN_BLINK_LEFT:
            print("Blink left")
        elif can_blink_position == CAN_BLINK_RIGHT:
            print("Blink right")

    if can_id == CAN_VELOCITY_ID:

        if v_print_guard == 20:
            can_v_lsb = can_data[4]
            can_v_msb = can_data[3]

            print("%u.%u\tmph" % (can_v_msb, can_v_lsb))
            v_print_guard = 0
        else:
            v_print_guard += 1

        # print("Velocoty: ", end = "")
        # for data in can_data:
        #     print("0x%X" % data, flush=True, end=' ')
        # print("")
