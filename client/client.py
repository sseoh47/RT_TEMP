import socket
import threading
import json
import time
from beacon import scan_for_beacons, found_beacon
from button import*
from constant import*
from sound import*

class Client():
    def __init__(self):
        self.running = True
        self.host = HOST  # 서버의 IP 주소
        self.port = PORT  # 서버의 포트 번호
        # 소켓 생성 및 서버에 연결
        # [OS ERROR 10038] 소켓으로 인한 에러 해결 -> 연결 지속하기에 소켓 하나만 사용하기로
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def send_data_to_server(self, data):
        try:
            self.sock.sendall(json.dumps(data).encode())
            # 서버로부터의 즉각적인 응답을 기다리지 않음
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
                
                # 파일이 존재하는지 확인합니다.
                if os.path.exists('./client/sample.wav'):
                    # 파일이 존재하면 send_file 함수를 실행합니다.
                    self.send_file('./client/sample.wav')
                else:
                # 파일이 존재하지 않으면 파일이 없다는 메시지를 출력합니다.
                    pass
                    
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
            self.sock.settimeout(None)  # 소켓의 타임아웃을 None으로 설정하여 무한 대기
            while self.running:
                response = self.sock.recv(1024).decode()  # 서버로부터 응답 수신
                if response:
                    print(f"Received from server: {response}")  # 수신된 응답 출력
                    self.check_bname(response)
                else:
                    break  # 서버로부터의 연결이 끊어졌을 경우 while 문을 종료
        except Exception as e:
            print(f"Error receiving data from server: {e}")

    def check_bname(self, response):
        if "bname changed from N/A to" in response:
            #print(found_beacon["name"])
            text_to_speech(found_beacon["name"])
            # 왜 사운드 재생이 안되지???
            button=BUTTON()
            button.record_dest()


    def send_file(self, file_path):
        file_size = os.path.getsize(file_path)
        self.send_data_to_server({"type": "file_transfer", "file_name": os.path.basename(file_path), "file_size": file_size})

        with open(file_path, 'rb') as file:
            while True:
                bytes_read = file.read(1024)
                if not bytes_read:
                    break  # 파일 전송 완료
                self.sock.sendall(bytes_read)
        
        # 파일 전송 완료 신호 보내기
        self.sock.sendall("done".encode())
        
        # 서버로부터의 응답 받기
        response = self.sock.recv(1024).decode()
        print(f"Server response: {response}")
        
        # 파일 전송이 완료된 후 파일 삭제
        os.remove(file_path)
        print(f"'{file_path}' has been successfully sent to the server and deleted.")



    def start(self):
        # 클라이언트 시작 메소드
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
            # 아래코드 응용해 두번째 버튼 기능 이용가능할듯?!
            # ctrlC일떄 아래 문구 출력, 소켓 닫고
            print("Program terminated")
            self.running = False
            self.sock.close()  # 프로그램 종료 시 소켓 닫기

if __name__ == '__main__':
    client = Client()
    client.start()