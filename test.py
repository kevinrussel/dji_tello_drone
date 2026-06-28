import time
import socket
import struct
udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = "192.168.10.2"
port = 8080
def takeoff_test():
    header = create_header()
    command = b"takeoff"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    time.sleep(5)
    header = create_header()
    command = b"land"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    pass

def create_header(flag):
    timestamp = time.time()
    if(flag == "land" or flag == "takeoff"):
        command_type = 's'
    else:
        command_type = 'd'
    header = struct.pack('!dc',timestamp,command_type)
    return header

takeoff_test()