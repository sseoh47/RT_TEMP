from bluepy.btle import Scanner, DefaultDelegate
import time

# 원하는 비콘의 이름
desired_name = "BUS"  # 여기에 원하는 비콘의 이름을 넣으세요

# 발견된 비콘 정보를 저장할 전역 변수
found_beacon = {"name": None, "rssi": None}

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        for (adtype, desc, value) in dev.getScanData():
            if adtype == 9 and value == desired_name:
                # print("Desired Beacon found:")
                # print("Name:", value)
                # print("RSSI:", dev.rssi)
                # 전역 변수에 정보 저장
                found_beacon["name"] = value
                found_beacon["rssi"] = dev.rssi
                return

scanner = Scanner().withDelegate(ScanDelegate())

def scan_for_beacons():
    scanner.scan(1.0)  # 1초 동안 스캔
    if found_beacon["name"]:
        return found_beacon
    else:
        return None

# try:
#     while True:
#         print("Scanning...")
#         result = scan_for_beacons()
#         if result:
#             print(f"Found Beacon: {result}")
#         time.sleep(1)  # 필요에 따라 스캔 간에 잠시 대기할 수 있음
# except KeyboardInterrupt:
#     print("Scanning stopped")
