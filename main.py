from djitellopy import Tello
import threading
import queue





def worker():
    while True:



def main():
    print("hello world")

    tello = Tello()
    tello.connect()

    udp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    udp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 4 * 1024 * 1024)
    udp_server_socket.bind(('',8080))
    udp_server_listen()


if __name__ == '__main__':
    main()
