import socket
import threading
import json
import time
from beacon import scan_for_beacons

class Client():
    def __init__(self):
        self.running = True
        self.host = "172.20.10.4"  # 서버의 IP 주소
        self.port = 8888  # 서버의 포트 번호
        self.found_beacon = {"name": None, "rssi": None}
        self.lock = threading.Lock()  # found_beacon에 대한 접근을 동기화하기 위한 Lock 객체 생성

    def send_data_to_server(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                sock.sendall(json.dumps(data).encode())
                # 서버로부터의 즉각적인 응답을 기다리지 않음
        except Exception as e:
            print(f"Could not send data to server: {e}")

    def update_beacon(self, name, rssi):
        with self.lock:  # found_beacon 사전에 안전하게 접근하기 위해 Lock 사용
            self.found_beacon["name"] = name
            self.found_beacon["rssi"] = rssi

    def data_sender(self):
        while self.running:
            with self.lock:
                if self.found_beacon["name"] is not None:
                    data = {
                        "bname": self.found_beacon["name"],
                        "rssi": self.found_beacon["rssi"],
                        "dest": None,
                        "busNum": -1
                    }
                    self.send_data_to_server(data)
            time.sleep(1)

    def beacon_scanner(self):
        try:
            while self.running:
                name, rssi = scan_for_beacons()  # scan_for_beacons 함수가 비콘의 이름과 rssi를 반환한다고 가정
                self.update_beacon(name, rssi)
        except Exception as e:
            print(f"Error during beacon scanning: {e}")
            self.running = False

    def listen_for_responses(self):
        """서버로부터 응답을 지속적으로 받는 메소드"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                sock.settimeout(None)  # 소켓의 타임아웃을 None으로 설정하여 무한 대기
                while self.running:
                    response = sock.recv(1024).decode()  # 서버로부터 응답 수신
                    if response:
                        print(f"Received from server: {response}")  # 수신된 응답 출력
                    else:
                        break  # 서버로부터의 연결이 끊어졌을 경우 while 문을 종료
        except Exception as e:
            print(f"Error receiving data from server: {e}")

    def start(self):
        """클라이언트 시작 메소드"""
        sender_thread = threading.Thread(target=self.data_sender)
        scanner_thread = threading.Thread(target=self.beacon_scanner)
        response_thread = threading.Thread(target=self.listen_for_responses)

        sender_thread.start()
        scanner_thread.start()
        response_thread.start()

        try:
            while sender_thread.is_alive() or scanner_thread.is_alive() or response_thread.is_alive():
                sender_thread.join(timeout=1)
                scanner_thread.join(timeout=1)
                response_thread.join(timeout=1)
        except KeyboardInterrupt:
            print("Program terminated")
            self.running = False

if __name__ == '__main__':
    client = Client()
    client.start()
