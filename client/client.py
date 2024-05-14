import socket
import threading
import json
import time
from beacon import scan_for_beacons, found_beacon

class Client():
    def __init__(self):
        self.running = True

    def send_data_to_server(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(("172.20.10.4", 8888))
                sock.sendall(json.dumps(data).encode())
                response = sock.recv(1024).decode()
                print(f"Received from server: {response}")
        except Exception as e:
            print(f"Could not send data to server: {e}")

    def data_sender(self):
        while self.running:
            if found_beacon["name"] is not None:
                data = {
                    "bname": found_beacon["name"],
                    "rssi": found_beacon["rssi"],
                    "dest": None,
                    "busNum": -1
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

if __name__ == '__main__':
    client = Client()
    sender_thread = threading.Thread(target=client.data_sender)
    scanner_thread = threading.Thread(target=client.beacon_scanner)
    sender_thread.start()
    scanner_thread.start()

    try:
        while sender_thread.is_alive() or scanner_thread.is_alive():
            sender_thread.join(timeout=1)
            scanner_thread.join(timeout=1)
    except KeyboardInterrupt:
        print("Program terminated")
        client.running = False
