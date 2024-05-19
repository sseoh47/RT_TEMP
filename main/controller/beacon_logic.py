import pandas as pd
import xml.etree.ElementTree as ET
import pandas as pd
import json

class Beacon_Model:
    # 중앙초교로 가고싶어.
    def __init__(self) -> None:
        self.__bus = [
            {'bname':'BUS',
             'name':'840',}
        ]



    # XML 파일 읽기
    def __get_bus(self):
        # XML PARSING
        tree = ET.parse('./data_set/bus_data.xml')
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
    
    def find_bus_with_bname(self, bname:str):
        result = "None"
        for bus in self.__bus:
            if bus['bname'] == bname:
                result = bus['name']
                break

        return result



class BeaconLogic:
    def __init__(self) -> None:
        self.__model = Beacon_Model()
        pass

    def find_beacon_info(self, bname:str) -> dict:
        result = {'root' : "BUS", 'body' : 'default'}
        bus_number = self.__model.find_bus_with_bname(bname)
        result['body'] = bus_number
        return result

