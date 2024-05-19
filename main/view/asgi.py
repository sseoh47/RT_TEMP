from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from view.tcp_socket import StreamTCPSocket
from controller.logic import Logic


HOST = '127.0.0.1'
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
            thread.start()

    
    def __client_handle_thread(self, streamTCPSocket):
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
        while True:
            dict_data = streamTCPSocket.receive()
            logic.recv_enque(dict_data=dict_data)

    def send_thread(self, streamTCPSocket:StreamTCPSocket, logic:Logic):
        while True:
            result = logic.isEmptySendQueue()
            if not result:
                dict_data = logic.send_deque()
                streamTCPSocket.send(dict_data=dict_data)
        