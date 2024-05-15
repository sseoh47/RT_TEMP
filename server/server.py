import socket
import threading
import json
import queue
from linkedList import *
from constant import*

class Server:
    def __init__(self):
        self.clients = LinkedList()  # 클라이언트 관리를 위한 LinkedList 인스턴스 생성
        self.last_data = {}  # 가장 최근에 받은 데이터를 저장할 변수 (키별로)
        self.data_queue = queue.Queue()  # 데이터 처리를 위한 큐

    # 데이터가 변경될 때 호출될 함수
    def data_changed(self, new_data):
        changes = []
        # 각 키에 대해서 이전 값과 새로운 값 비교
        for key in new_data:
            if key not in self.last_data or self.last_data[key] != new_data[key]:
                changes.append(f"{key} changed from {self.last_data.get(key, 'N/A')} to {new_data[key]}")
                self.last_data[key] = new_data[key]  # 가장 최근 데이터 갱신
        
        return changes

    # 데이터를 처리하는 함수
    def process_data(self):
        while True:
            client_socket, data = self.data_queue.get()
            changes = self.data_changed(data)
            if changes:
                change_message = "\n".join(changes)
                print("Data changed:")
                print(change_message)
                client_socket.sendall(change_message.encode())
            else:
                print("No data change detected.")
                client_socket.sendall("No data change detected.".encode())
            print("-------------------------------------------\n")

    # 클라이언트 핸들링 함수
    def handle_client(self, client_socket, addr):
        with client_socket:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                data = json.loads(data)  # json 문자열을 Python 사전으로 변환
                print(f"Received: {data}")
                # 데이터 큐에 추가
                self.data_queue.put((client_socket, data))
        self.clients.remove(client_socket)  # 클라이언트 연결 종료 시 LinkedList에서 제거

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server started. Waiting for client connections...")

        # 데이터 처리 스레드 시작
        processing_thread = threading.Thread(target=self.process_data)
        processing_thread.start()

        while True:
            client_socket, addr = server_socket.accept()
            self.clients.add(client_socket, addr)  # 새 클라이언트 추가
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

if __name__ == '__main__':
    server = Server()
    server.start_server()
