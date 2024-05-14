import socket
import threading
import json
import time
from beacon import*


class Client():
    def __init__(self):
        self.running = True  # 스레드 실행 상태를 제어하는 플래그

    def send_data_to_server(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('127.0.0.1', 8888))
            sock.sendall(json.dumps(data).encode())  # Python 사전을 json 문자열로 변환하여 전송
            response = sock.recv(1024).decode()
            print(f"Received from server: {response}")

    def data_sender(self):
        data = {"bname": None, "rssi": -1, "dest": None, "busNum": -1}
        while self.running:  # self.running을 사용하여 반복문 제어
            try:
                data["bname"] = found_beacon["name"]
                data["rssi"]=found_beacon["rssi"]
                self.send_data_to_server(data)
                time.sleep(1)  # 1초마다 데이터 전송
            except Exception as e:
                print(f"Error: {e}")
                self.running = False

if __name__ == '__main__':
    client = Client()
    sender_thread = threading.Thread(target=client.data_sender)
    sender_thread.start()
    try:
        while sender_thread.is_alive():  # 샌더 스레드가 살아있는 동안 대기
            sender_thread.join(timeout=1)  # 1초마다 인터럽트 체크
    except KeyboardInterrupt:
        print("Program terminated")
        client.running = False  # 스레드 종료를 위해 running 플래그를 False로 설정
        sender_thread.join()  # 스레드가 완전히 종료될 때까지 대기