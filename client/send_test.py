from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen()

    client_socket, _  = server_socket.accept()
    r_thread= Thread(target=recv_thread, args=(client_socket,))
    s_thread= Thread(target=send_thread, args=(client_socket,))

    r_thread.start()
    s_thread.start()

def recv_thread(client_socket:socket):
    while True:
        data = client_socket.recv(1024).decode()
        print(data)
    
def send_thread(client_socket:socket):
    while True:
        # root body
        send_data = "root body"
        print(send_data)
        client_socket.send(send_data.encode())






if __name__ == "__main__":
    main()