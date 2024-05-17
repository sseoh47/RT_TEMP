import os
from client import*

def send_file(self, file_path):
    print("*")
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
        
    # 파일 전송이 완료된 후 파일 삭제
    os.remove(file_path)
    print(f"'{file_path}' has been successfully sent to the server and deleted.")