import pandas as pd
import xml.etree.ElementTree as ET
import pandas as pd

def make_xml():
    bname = 'bname'
    name = 'name'
    x = 'x'
    y = 'y'
    
    # 데이터
    data = [
        {bname: 'STATION', name: '영남대건너', y: '35.836909', x: '128.753671'},
        {bname: '2', name: '경산시청', y: '35.825358', x: '128.753026'}
    ]

    # XML 요소 생성
    root = ET.Element("data")

    for row_data in data:
        row_element = ET.SubElement(root, "row")

        for key, value in row_data.items():
            element = ET.SubElement(row_element, key)
            element.text = value

    # XML 트리 생성
    tree = ET.ElementTree(root)

    # XML 파일로 저장
    tree.write("station_data.xml")


def show_xml():
    # XML 파일 읽기
    tree = ET.parse('./station_data.xml')
    root = tree.getroot()

    # XML 데이터 파싱하여 Pandas DataFrame으로 변환
    data = []
    for child in root:
        row = {}
        for subchild in child:
            row[subchild.tag] = subchild.text
        data.append(row)

    df = pd.DataFrame(data)
    #result = df[(df['bid'] == '1')].loc['x']
    print(df)
    

if __name__ == "__main__":
    make_xml()
    show_xml()
