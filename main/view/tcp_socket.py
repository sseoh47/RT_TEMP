from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue
from view.protocol import CustomProtocol

class StreamTCPSocket:
    def __init__(self, client_socket, addr):
        self.__client_socket:socket = client_socket
        self.__addr = addr
        self.__protocol = CustomProtocol()
        return
    
    def receive(self):
        message = self.__client_socket.recv(1024)
        dict_data = self.__protocol.string_to_dict(message.decode())
        return dict_data

        # data = "root data"
    def send(self, dict_data):
        data:str = self.__protocol.dict_to_string(dict_data=dict_data)
        self.__client_socket.send(data.encode())
        return