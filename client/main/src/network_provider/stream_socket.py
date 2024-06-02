from socket import socket


class StreamTCPSocket:
    def __init__(self, client_socket) -> None:
        self.__socket:socket = client_socket
        pass

    def recv(self)->bytes:
        recv_data:bytes = self.__socket.recv(1024)
        #print(recv_data)
        return recv_data
    
    def send(self, string_data:str):
        self.__socket.send(string_data.encode())
        return