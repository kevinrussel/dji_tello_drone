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
            timestamp,command_type,header_message =(self.deal_with_packet(message))
            print("hello")
            print(timestamp)
            print(self.last_known_time)
            if timestamp > self.last_known_time:
                message = [command_type,header_message]
                print(message)
                self.command_queue.put(message)
            else:
                continue
            
    def start_drone(self):
        try:
            self.tello.connect()
        except Exception:
            return Exception

    def deal_with_packet(self,message):
        header = message[:9]
        timestamp,command_type = struct.unpack("!Qc", header)
        command_type = command_type.decode("utf-8")
        header_message = (message[9:]).decode("utf-8")          
        return timestamp,command_type,header_message 

    def drone_commands(self):
        while True:
            command = self.command_queue.get()
            if command is None:
                break
            else:
                command_type = command[0]
                command = command[1]
                if(command_type == 's'):
                    print("hitting")
                    if(command == "takeoff"):
                        self.tello.takeoff()
                    elif command == "land":
                        self.tello.land()
                ## TODO: FIX THIS   
                elif (command_type == 'd'):
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
drone.main()