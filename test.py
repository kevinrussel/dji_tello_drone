import time
import socket
import struct
udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = "192.168.10.2"
port = 8080


def create_header(flag):
    timestamp = time.time_ns()
    if(flag == "land" or flag == "takeoff"):
        command_type = b's'
    else:
        command_type = b'd'
    header = struct.pack('!Qc',timestamp,command_type)
    return header


def test1_takeoff():
    header = create_header("takeoff")
    command = b"takeoff"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    time.sleep(5)
    header = create_header("land")
    command = b"land"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    pass

def test2_altitude():
    pass


test1_takeoff()