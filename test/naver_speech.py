import json
import requests

data = open("./test.wav", "rb") # STT를 진행하고자 하는 음성 파일

Lang = "Kor" # Kor / Jpn / Chn / Eng
#URL = "https://naveropenapi.apigw.ntruss.com/recog/v0/stt?lang=" + Lang
URL = "https://clovaspeech-gw.ncloud.com/recog/v1/stt?lang=" + Lang

ID = "alsrhks2508" # 인증 정보의 Client ID
Secret = "21bdbb764e5d4f3da460a9c37dbf58af" # 인증 정보의 Client Secret
    
headers = {
    "Content-Type": "application/octet-stream", # Fix
    "X-CLOVASPEECH-API-KEY" : Secret
}
response = requests.post(URL,  data=data, headers=headers)
rescode = response.status_code

if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)