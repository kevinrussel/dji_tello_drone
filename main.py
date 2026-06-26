from djitellopy import Tello
import threading
import queue
import socket


class tello_class:

    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.udp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 4 * 1024 * 1024)
        self.udp_server_socket.bind(('',8080))

    def worker():
        while True:
            pass


    def main(self):
        print("hello world")
        tello = Tello()
        tello.connect()
        
        udp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        udp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 4 * 1024 * 1024)
        udp_server_socket.bind(('',8080))
        udp_server_listen()


drone = tello_class()
