import pandas as pd
import xml.etree.ElementTree as ET
import pandas as pd
import requests

# TMAP_APPKEY="6vggxo848T2ilJW9rBGDy1QgTrufgNimagn5fPiH"
TMAP_APPKEY = "wuLynpCfphaaJZkwoId0w4AWaJb9mbht1IVtIX0K"  # __ 혜림
# TMAP_APPKEY = "P56mSqdnljg7fNjmu2BD5I1DEutBPcVazegTouZ8" # __ 선배

class Master_Model:
    def __init__(self):
        print("SYSTEM_CALL||Master_Model_Created")
        self.station:pd.DataFrame = self.__get_station() 
        
    # XML 파일 읽기
    def __get_station(self):
        # XML PARSING
        tree = ET.parse('./model/data_set/station_data.xml')
        root = tree.getroot()

        # XML 데이터 파싱하여 Pandas DataFrame으로 변환
        data = []
        for child in root:
            row = {}
            for subchild in child:
                row[subchild.tag] = subchild.text
            data.append(row)

        # DataFrame으로 변경하여 보관
        df = pd.DataFrame(data)
        return df
    
    # DataFrame 보여주기
    def show_df(self, bname = "1"):
        print(self.station)
        
    # 경로 데이터 가지고오기
    def get_coord(self, bname = "-1"):    
        # bname가 같은 줄에서 "name" 뽑아오기
        target = self.station.loc[self.station['bname'] == bname, 'name'].values[0]
        x = self.station.loc[self.station['bname'] == bname, 'x'].values[0]
        y = self.station.loc[self.station['bname'] == bname, 'y'].values[0]

        # Target 객체로 변경 후 보관 및 리턴
        result = Target(target=target, type = True, x=x, y=y)
        return result
    
    # Target 객체 생성(저장되어 있던 타겟)
    def make_target(self, target):
        target_place:Target = Target(target=target)
        return target_place

        
class Target():
    def __init__(self, target, type = False, x = "0", y = "0"):
        self.name= target
        # x, y를 매게변수로 받아서 만들때
        if type:
            self.x=x
            self.y=y
        # x, y를 Tmap에서 받은 후 만들때
        else:
            # Tmap에 경도, 위도 요청
            result_x, result_y = self.__get_data_from_TMAP()
            self.x = result_x
            self.y = result_y
            
    # Tmap에 경도 위도 요청
    def __get_data_from_TMAP(self):
        version = 1
        url = f"https://apis.openapi.sk.com/tmap/pois?version={version}&searchKeyword={self.name}&appKey={TMAP_APPKEY}"
        result = requests.get(url)
        result = result.json()  # 바디 데이터 

        # 목표 지점의 정중앙 좌표
        x = result["searchPoiInfo"]["pois"]["poi"][0]["noorLon"]
        y = result["searchPoiInfo"]["pois"]["poi"][0]["noorLat"]
        return x, y
        
