import socket
import threading
import json
from linkedList import*

class Server:
    def __init__(self):
        self.clients = LinkedList()  # 클라이언트 관리를 위한 LinkedList 인스턴스 생성

    # 데이터가 변경될 때 호출될 함수
    def data_changed(self, new_data):
        print(f"Data changed: {new_data}")

    # 클라이언트 핸들링 함수
    def handle_client(self, client_socket, addr):
        with client_socket:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                data = json.loads(data)  # json 문자열을 Python 사전으로 변환
                print(f"Received: {data}")
                # 데이터 변경 확인 및 처리
                self.data_changed(data)
                # 클라이언트에게 응답 보내기
                client_socket.sendall(json.dumps(data).encode())
        self.clients.remove(client_socket)  # 클라이언트 연결 종료 시 LinkedList에서 제거

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("172.20.10.4", 8888))
        server_socket.listen()
        print("Server started. Waiting for client connections...")

        while True:
            client_socket, addr = server_socket.accept()
            self.clients.add(client_socket, addr)  # 새 클라이언트 추가
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

if __name__ == '__main__':
    server = Server()
    server.start_server()
