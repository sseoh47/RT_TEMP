from bluepy.btle import Scanner, DefaultDelegate
from threading import Thread
import os
# from button import*

BUS = "840"  
STATION = "STATION"  # 다시 확인하기

class BeaconNetwork:
    def __init__(self) -> None:
        self.__beacon_data = [
            {"bname" : "STATION", "rssi" : 0},
            {"bname" : "BUS", "rssi" : 0}]
        self.__beacon_name = self.__beacon_data[0]["bname"]
        self.__bus_beacon_name = self.__beacon_data[1]["bname"]
        self.__beacon_rssi = self.__beacon_data[1]["rssi"]
        self.__scanner = Scanner().withDelegate(ScanDelegate(self.__beacon_data))
        thread = Thread(target=self.find_beacon_thread)
        thread.start()
        return
    
    def get_beacon_data(self):
        return self.__beacon_data
    
    def get_beacon(self):
        return self.__beacon_name
    
    def get_rssi(self):
        return self.__beacon_rssi
    
    def get_bus_beacon(self):
        return self.__bus_beacon_name

    def find_beacon_thread(self):
        while True:
            self.__scanner.scan(1.0)
        
class ScanDelegate(DefaultDelegate):
    def __init__(self, beacon_list):
        DefaultDelegate.__init__(self)
        self.search_mode = 'STATION'  # ++5/14++ 처음에는 STATION 비콘을 찾도록 설정
        self.beacon_list = beacon_list
        print("beacon init")

    def handleDiscovery(self, dev, isNewDev, isNewData):
        try:
            for (adtype, desc, value) in dev.getScanData():
                if value == STATION:
                    # STATION 비콘 발견
                    print("STATION Beacon found")
                    self.beacon_list[0]['bname'] = value
                    self.beacon_list[0]['rssi'] = dev.rssi
                elif value == BUS:
                    # BUS 비콘 발견
                    print("BUS Beacon found")
                    self.beacon_list[1]['bname'] = value
                    self.beacon_list[1]['rssi'] = dev.rssi

        except KeyboardInterrupt:
            print("Scanning stopped")
            
        except Exception as e:
            print(f"Error occurred while receiving message: {e}")



