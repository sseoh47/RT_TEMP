from model import Master_Model, Target, TMAP_APPKEY
import requests

class PathFindLogic:
    def __init__(self) -> None:
        self.model:Master_Model = Master_Model() # 마스터 모델
    

    # 최단 경로 계산
    def get_shortest_path(self, bname:str= '-1', target:str = "default"):
        print(f"SYSTEM_CALL||bname:{bname}and_Target:{target}_inserted")

        # 예외처리 return 문
        if bname == '-1' or target == "default":
            return 
        
        # 경로 검색기 생성
        path_finder = Path_Finder()
        
        # String 형태로 타입 변경
        bname = str(bname)

        # 현재 위치와 목표 위치 설정
        now_place:Target = self.model.get_coord(bname)
        target_place:Target = self.model.make_target(target=target)
        print("now_place :", now_place.x)
        print("target_place :", target_place.x)

        # Tmap 대중교통 경로 검색
        bus = path_finder.path_finding(now_place=now_place, target_place=target_place)
    
        # 버스를 찾지 못했을 때
        if bus == "None":
            return {"result": f"{target}로 갈수 있는 버스는 없습니다. 죄송합니다."}
        
        # 버스 찾았을 때 Dict 형태로 반환 데이터 준비
        return_data = f"{target}으로 가기 위해 {bus}"
        return_data = return_data + "번 버스를 타야합니다. 감사합니다."
            
        result = {'root' : 'PATH', "body":return_data}
        return result 

class Path_Finder:
    def __init__(self):
        print("SYSTEM_CALL||Welcome_Path_Finder")
        
    def path_finding(self, now_place:Target, target_place:Target):
        # Tmap 대중교통 url
        api_url = "https://apis.openapi.sk.com/transit/routes"
        
        # 전송할 데이터 (헤더)
        headers = {
            "accept": "application/json",  # JSON 형식으로 데이터
            "appKey": TMAP_APPKEY,  # 인증 토큰
            "content-type":"application/json"
        }
    
        """ headers
        - accept : application/json
        - appKey : 발급 Appkey
        - content-type : application/json
        """

        # 전송할 데이터 (바디)
        body = {
            "startX": str(now_place.x),
            "startY": str(now_place.y),
            "endX": str(target_place.x),
            "endY": str(target_place.y),
            "count" : 1,
            "lang": 0,
            "format":"json"
        }
        
        """ body
        {
            "startX": "127.02550910860451",
            "startY": "37.63788539420793",
            "endX": "127.030406594109",
            "endY": "37.609094989686",
            "count" : 1,
            "lang": 0,
            "format":"json"
        }
        """

        # POST 요청 보내기
        response = requests.post(api_url, headers=headers, json=body)
        response = response.json()  # 돌아온 데이터 바디
        try:
            # 버스 한개만 가지고 온다
            result = self.__get_data_from_response(response=response)
        except Exception as e:
            result = "None"
        
        # bus정보의 리스트
        return result
        

    def __get_data_from_response(self, response:dict):
        bus:list = response["metaData"]["plan"]["itineraries"][0]["legs"][1]["route"]
        return bus




