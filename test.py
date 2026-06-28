import time
import socket
import struct
udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = 
port = 
def takeoff_test():
    header = create_header()
    command = b"takeoff"
    message = header + command
    udp_client_socket.sendto(message(server_address,port))
    
    
    pass

def create_header():
    timestamp = time.time()
    header = struct.pack('!d',timestamp)
    return header