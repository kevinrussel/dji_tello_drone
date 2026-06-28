from djitellopy import Tello
import threading
import queue
import socket
import struct

class tello_class:
    command_queue = queue.Queue()
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.udp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 4 * 1024 * 1024)
        self.udp_server_socket.bind(('',8080))

    def worker(self):
        while True:
            pass

    def start_drone(self):
        try:
            self.tello.connect()
        except Exception:
            return Exception

    def deal_with_header(self,message):
        header = message[:10]
        packet_num,timestamp = struct.unpack("!Hd", header)
        timestamp = time.time() - timestamp
        message = (message[10:]).decode("utf-8")
                   
        return packet_num,timestamp,message 

    def drone_commands(self):
        while True:
            command = self.command_queue.get()
            if command is None:
                break
            else:
                direction = command[0]
                distance = command[1]
                self.tello.move(direction,distance)


    def main(self):
        tello = Tello()
        thread = threading.Thread(target=self.worker,daemon=True)
        thread.start()
        self.start_drone()
        


drone = tello_class()
