import socket
import threading
import json
import time
import os  # os 모듈 추가
from beacon import scan_for_beacons, found_beacon
from button import BUTTON
from constant import HOST, PORT
from sound import text_to_speech

class Client:
    def __init__(self):
        self.running = True
        self.host = HOST
        self.port = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_data_to_server(self, data):
        try:
            # 파일이 존재하는지 확인합니다.
            if os.path.exists('./sample.wav'):
                # 파일이 존재하면 send_file 함수를 실행합니다.
                self.send_file('./sample.wav')
            else:
                # 파일이 존재하지 않으면 파일이 없다는 메시지를 출력합니다.
                pass
            self.sock.sendall(json.dumps(data).encode())
        except Exception as e:
            print(f"Could not send data to server: {e}")

    def data_sender(self):
        while self.running:
            if found_beacon["name"] is not None:
                data = {
                    "bname": found_beacon["name"],
                    "rssi": found_beacon["rssi"],
                    "dest": None,
                    "busNum": -1,
                }
                self.send_data_to_server(data)
            time.sleep(1)

    def beacon_scanner(self):
        try:
            while self.running:
                scan_for_beacons()
        except Exception as e:
            print(f"Error during beacon scanning: {e}")
            self.running = False

    def listen_for_responses(self):
        try:
            self.sock.settimeout(None)
            while self.running:
                response = self.sock.recv(1024).decode()
                if response:
                    print(f"Received from server: {response}")
                    self.check_bname(response)
                else:
                    break
        except Exception as e:
            print(f"Error receiving data from server: {e}")

    def check_bname(self, response):
        if "bname changed from N/A to" in response:
            text_to_speech(found_beacon["name"])
            button = BUTTON()
            button.record_dest()

    def send_file(self, file_path):
        try:
            file_size = os.path.getsize(file_path)
            self.sock.sendall(json.dumps({"type": "file_transfer", "file_name": os.path.basename(file_path), "file_size": file_size}).encode())

            with open(file_path, 'rb') as file:
                while True:
                    bytes_read = file.read(1024)
                    if not bytes_read:
                        break
                    self.sock.sendall(bytes_read)

            self.sock.sendall("done".encode())

            response = self.sock.recv(1024).decode()
            print(f"Server response: {response}")
            os.remove(file_path)
            print(f"'{file_path}' has been successfully sent to the server and deleted.") # 클라이언트는 여기까지 확인
            # 이후 Broken Pipe
        except Exception as e:
            print(f"Could not send file to server: {e}")

    def start(self):
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
            self.sock.close()

if __name__ == '__main__':
    client = Client()
    client.start()
