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
        self.takeoff_initiated = False


    def worker(self):
        while True:
            message,address = self.udp_server_socket.recvfrom(100)
            timestamp,command_type,command_speed = (self.deal_with_packet(message))
            
            if timestamp > self.last_known_time:
                message = [command_type,command_speed]
                self.command_queue.put(message)
        
            
    def start_drone(self):
        try:
            self.tello.connect()
        except Exception:
            return Exception

    def deal_with_packet(self,message):
        timestamp,command_type,command_speed = struct.unpack("!Qch", message)
        command_type = command_type.decode("utf-8")         
        return timestamp,command_type,command_speed 

    def drone_commands(self):
        while True:
            command = self.command_queue.get()
            if command is None:
                break
            else:
                command_type = command[0]
                command_speed = command[1]
                if(command_type == 't'):
                    if(not self.takeoff_initiated):
                        self.takeoff_initiated = True
                        self.tello.takeoff()
                if(self.takeoff_initiated):                    
                    if command_type == "l":
                        self.tello.land()   
                    elif (command_type == 'm'):
                        self.tello.send_rc_control(0,0,command_speed,0)
                        print(self.tello.get_speed_x())
                        


    def main(self):
        tello = Tello()
        thread = threading.Thread(target=self.worker,daemon=True)
        thread.start()
        self.start_drone()
        self.drone_commands()
        


drone = tello_class()
drone.main()