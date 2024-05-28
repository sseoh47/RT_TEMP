from bluepy.btle import Scanner, DefaultDelegate
from client import*  # 클라이언트 코드를 import
from constant import*
import os
# from button import*


BUS = "BUS"  
STATION = "YU_UNIV"  # 다시 확인하기

class ScanDelegate(DefaultDelegate):
    def __init__(self, client):
        DefaultDelegate.__init__(self)
        self.client = client
        self.search_mode = 'STATION'  # ++5/14++ 처음에는 STATION 비콘을 찾도록 설정
        print("beacon init")

    def handleDiscovery(self, dev, isNewDev, isNewData):
        try:
            for (adtype, desc, value) in dev.getScanData():
                # ++5/14++
                if adtype == 9:
                    if self.search_mode == 'STATION' and value == STATION:
                        # STATION 비콘 발견
                        print("STATION Beacon found")
                        self.client.send_beacon(value, dev.rssi)
                        self.search_mode = 'BUS'  # 이제 BUS 비콘을 찾도록 상태 변경
                    elif self.search_mode == 'BUS' and value == BUS:
                        # BUS 비콘 발견
                        print("BUS Beacon found")
                        self.client.send_beacon(value, dev.rssi)
                # ++++
                
                # if adtype == 9 and value in [BUS, STATION]:
                #     #print("Name:", value)
                #     #print("RSSI:", dev.rssi)
                #     # 직접 send_beacon 호출
                #     self.client.send_beacon(value, dev.rssi)

        except KeyboardInterrupt:
            print("Scanning stopped")
            
        except Exception as e:
            print(f"Error occurred while receiving message: {e}")

    def send_beacon_in_thread(self, beacon_name, rssi):
        if self.current_thread and self.current_thread.is_alive():
            self.is_active = False  # 현재 스레드에 종료 요청
            self.current_thread.join()  # 현재 스레드가 종료될 때까지 기다림

        self.is_active = True
        # Client 인스턴스의 send_beacon 메소드를 호출
        self.current_thread = threading.Thread(target=self.client.send_beacon, args=(beacon_name, rssi))
        self.current_thread.start()


if __name__ == "__main__":
    client = Client(SERVER_HOST, PORT)  # 이 부분에서 Client 클래스를 인스턴스화
    #print("환경변수:",os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    scanner = Scanner().withDelegate(ScanDelegate(client))  # Client 인스턴스를 ScanDelegate에 전달
    try:
        while True:
            print("scanner while")
            devices = scanner.scan(1.0)  # 2초 동안 스캔

    except KeyboardInterrupt:
        print("scann stop")