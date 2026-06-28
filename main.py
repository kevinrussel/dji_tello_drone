from djitellopy import Tello
import threading
import queue
import socket
import struct
import time
class tello_class:
    command_queue = queue.Queue()
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.udp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 4 * 1024 * 1024)
        self.udp_server_socket.bind(('',8080))
        self.last_known_time = time.time_ns()


    def worker(self):
        while True:
            message,address = self.udp_server_socket.recvfrom(100)
            message = (self.deal_with_header(message)).split()
            self.command_queue.put(message)
            
    def start_drone(self):
        try:
            self.tello.connect()
        except Exception:
            return Exception

    def deal_with_header(self,message):
        header = message[:8]
        timestamp = struct.unpack("!d", header)
        timestamp = time.time() - timestamp
        header_message = (message[8:]).decode("utf-8")          
        return timestamp,header_message 

    def drone_commands(self):
        while True:
            command = self.command_queue.get()
            if command is None:
                break
            else:
                if(command == "takeoff"):
                    self.tello.take()
                else:
                    direction = command[0]
                    distance = command[1]
                    self.tello.move(direction,distance)


    def main(self):
        tello = Tello()
        thread = threading.Thread(target=self.worker,daemon=True)
        thread.start()
        self.start_drone()
        self.drone_commands()
        


drone = tello_class()
