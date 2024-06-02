from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from view.tcp_socket import StreamTCPSocket
from controller.logic import Logic
import time


HOST = '172.20.10.4'
PORT = 5000

class ASGI:
    def __init__(self):
        print("Start ASGI")

    def start(self):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            client_socket, addr = server_socket.accept()
            streamTCPSocket = StreamTCPSocket(client_socket=client_socket, addr=addr)
            thread = Thread(target=self.__client_handle_thread,
                            args=(streamTCPSocket,))
            print("connected, and thread start")
            thread.start()

    
    def __client_handle_thread(self, streamTCPSocket):
        print("client handle thread started")
        logic = Logic()

        recv_thread = Thread(target=self.recv_thread,
                             args= (streamTCPSocket, logic))
        send_thread = Thread(target=self.send_thread,
                             args= (streamTCPSocket, logic))

        recv_thread.start()
        send_thread.start()

        recv_thread.join()
        send_thread.join()

    def recv_thread(self, streamTCPSocket:StreamTCPSocket, logic:Logic):
        print("recv thread started")
        while True:
            time.sleep(0.2)
            dict_data = streamTCPSocket.receive()
            logic.recv_enque(dict_data=dict_data)

    def send_thread(self, streamTCPSocket:StreamTCPSocket, logic:Logic):
        print("send thread started")
        while True:
            time.sleep(0.2)
            result = logic.isEmptySendQueue()
            if not result:
                dict_data = logic.send_deque()
                streamTCPSocket.send(dict_data=dict_data)
        