import time
import socket
import struct
udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def takeoff_test():
    header = create_header()
    
    
    
    pass

def create_header():
    timestamp = time.time()
    header = struct.pack('!d',timestamp)
    return header