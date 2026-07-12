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
    header = create_header("takeoff")
    command = b"takeoff"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    time.sleep(10)
    header = create_header("up")
    command = b"up"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    time.sleep(5)

    header = create_header("up")
    command = b"up"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    time.sleep(5)

    header = create_header("down")
    command = b"down"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    time.sleep(5)

    header = create_header("down")
    command = b"down"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    time.sleep(5)
    header = create_header("land")
    command = b"land"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    


def test3_up_and_down():
    header = create_header("takeoff")
    command = b"takeoff"
    message = header + command
    udp_client_socket.sendto(message,(server_address,port))
    time.sleep(10)





# test1_takeoff()
test2_altitude()