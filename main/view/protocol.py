
class CustomProtocol:
    def __init__(self):
        return

    # 송신 받은 데이터 분석하기
    # data = "BUS 509 dumy"   버스 비콘 누구세요? 하는 데이터
    # data = "PATH STATION TARGET"  내가 있는곳에서 타야하는 버스 찾기 데이터
    #splited_data = ["root", '경산 시청']
    def string_to_dict(self, string_data:str) -> dict:
        try:
            splited_data = string_data.split(' ', 3)
            dict_data  = {
                'root' : splited_data[0],
                'bname' : splited_data[1],
                'body' : splited_data[2]
            }
        except Exception as e:
            dict_data = {'root': "bad_request",
                         'bname': '-1',
                         'body': e}
        finally:
            return dict_data
        
    

    # dict_data {"root": :"root", "body":"body"}
    # str_data = "root body"
    def dict_to_string(self, dict_data:dict) -> str:
        try:
            string_data = ""
            for value in dict_data.values():
                string_data += value
                string_data += " "
        except Exception as e:
            string_data = f"error {e}"

        finally:
            return string_data

        # dict_data = "PATH 840"