import time
import socket
import struct
udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = "192.168.10.2"
port = 8080


def create_header(flag):
    timestamp = time.time_ns()
    speed = 60
    if( flag == "takeoff"):
        command_type = b't'
    elif (flag == "land"):
        command_type = b'l'
    elif flag == "up":
        speed = 60
        command_type = b'm'
    else:
        command_type = b'm'
        speed = -60
    header = struct.pack('!Qch',timestamp,command_type,speed)
    return header


def test1_takeoff():
    header = create_header("takeoff")
    command = b"takeoff"
    message = header + command
    udp_client_socket.sendto(header,(server_address,port))
    time.sleep(5)
    header = create_header("land")
    command = b"land"
    message = header + command
    udp_client_socket.sendto(header,(server_address,port))
    pass

def test2_altitude():
    header = create_header("takeoff")
    command = b"takeoff"
    message = header + command
    udp_client_socket.sendto(header,(server_address,port))
    time.sleep(10)
    header = create_header("up")
    command = b"up"
    message = header
    udp_client_socket.sendto(header,(server_address,port))
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
    udp_client_socket.sendto(header,(server_address,port))
    time.sleep(5)
    position ="up"
    for i in range(1,30):
        if(i % 3 == 0):
            if(position == "up"):
                position = "down"
            else:
                position = "up"
        command = create_header(position)
        udp_client_socket.sendto(command,(server_address,port))
        time.sleep(0.5)    
    header = create_header("land")
    udp_client_socket.sendto(header,(server_address,port))






# test1_takeoff()
# test2_altitude()
test3_up_and_down()