import socket
import threading
import json
from queue import Queue
from linkedList import *
from constant import*

class Server:
    def __init__(self):
        self.clients = LinkedList()  # 클라이언트 관리를 위한 LinkedList 인스턴스 생성
        self.last_data = {}  # 가장 최근에 받은 데이터를 저장할 변수 (키별로)
        self.data_queue = Queue()  # 데이터 처리를 위한 큐

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
            try:
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
            except Exception as e:
                print(f"Error processing data: {e}")
                continue

    def handle_client(self, client_socket, addr):
        with client_socket:
            client_socket.settimeout(60)  # 타임아웃 설정 (60초)
            receiving_file = False  # 파일 수신 상태 플래그
            file_name = None
            file_size = 0
            received_size = 0

            while True:
                try:
                    data = client_socket.recv(1024)  # 데이터를 바이너리 형태로 받음
                    if not data:
                        break
                        
                    if receiving_file:
                        # 파일 데이터 수신 상태에서는 바로 파일에 쓰기
                        with open(file_name, 'ab') as f:
                            f.write(data)
                        received_size += len(data)
                        if received_size >= file_size:
                            # 파일 전송 완료
                            print("File transfer completed.")
                            receiving_file = False
                            received_size = 0
                        continue

                    try:
                        # 데이터를 UTF-8로 디코드하여 JSON으로 변환
                        data_str = data.decode('utf-8')
                        data = json.loads(data_str)
                    except UnicodeDecodeError:
                        continue  # 디코드 실패시 무시 (일반적인 경우 발생하지 않음)
                    except json.JSONDecodeError:
                        print("JSON Decode Error: 데이터 형식이 올바르지 않습니다.")
                        continue

                    print(f"Received: {data}")

                    if data.get("type") == "file_transfer":
                        file_name = data["file_name"]
                        file_size = data["file_size"]
                        receiving_file = True  # 파일 수신 상태로 전환
                        print(f"Receiving file: {file_name}, size: {file_size} bytes")
                        with open(file_name, 'wb') as f:
                            pass  # 파일 초기화 (기존 파일 내용 삭제)
                    else:
                        # 데이터 큐에 추가
                        self.data_queue.put((client_socket, data))

                except socket.timeout:
                    print(f"Connection with {addr} timed out.")
                    break
                except Exception as e:
                    print(f"Error handling client {addr}: {e}")
                    break

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
            try:
                client_socket, addr = server_socket.accept()
                self.clients.add(client_socket, addr)  # 새 클라이언트 추가
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.start()
            except Exception as e:
                print(f"Error accepting client connection: {e}")

if __name__ == '__main__':
    server = Server()
    server.start_server()
