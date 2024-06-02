from queue import Queue
from controller.beacon_network import BeaconNetwork
from controller.hardware_ctrl import HardwareCtrlClass, MIC_BUTTON, END_BUTTON, SPEAK_BUTTON
from threading import Thread
import RPi.GPIO as GPIO
import json
import requests


from gtts import gTTS
#import speech_recognition as sr
import re  # String 분석용도 
import time



class EmbeddedLogic:
    def __init__(self) -> None:
        self.__recv_queue=Queue()
        self.__send_queue=Queue()
        self.__now_state = "default"  # PATH or BUS or default
        self.__beacon_network = BeaconNetwork()
        self.__harward_ctrl = HardwareCtrlClass()
        self.__target_location = ""
        thread = Thread(target=self.start_logic)
        thread.start()

    def start_logic(self):
        print("logic 시작")
        while True:
            thread = Thread(target=self.embedded_logic_thread)
            thread.start()
            thread.join()
            print("logic 종료됨")
            print("logic 재시작 됨")

        
    # send queue가 비어있는지 확인-> YES(1)/NO(0)로 응답(bool)
    def is_send_queue_empty(self)->bool:  # bool로 반환
        result=self.__send_queue.empty()
        return result

    # recv queue가 비어있는지 확인-> YES(1)/NO(0)로 응답(bool)
    def __is_recv_queue_empty(self)->bool:  # bool로 반환
        result=self.__recv_queue.empty()
        return result

    # recv thread's enque
    def recv_enque(self, dict_data:dict):
        print(dict_data)
        self.__recv_queue.put(dict_data)

    def __send_enque(self, dict_data:dict):
        print(dict_data)
        self.__send_queue.put(dict_data)

    # recv thread's deque
    def send_deque(self)->dict:
        dict_data = self.__send_queue.get()
        print(dict_data)
        return dict_data

    def __recv_deque(self)->dict:
        dict_data = self.__recv_queue.get()
        print(dict_data)
        return dict_data
    
    # 받아온 데이터를 스피커로 말할 문장 생성 함수
    def __make_sentence(self, data):
        # 버스를 찾지 못했을 때
        if data == "None":
            return {"result": f"{self.__target_location}로 갈 수 있는 버스는 없습니다. 죄송합니다."}
        
        # 버스 찾았을 때 :: Dict 형태로 반환 데이터 준비
        sentence_data = f"{self.__target_location}으로 가기 위해 {data}"
        sentence_data = sentence_data + "번 버스를 타야 합니다. 감사합니다."
        return sentence_data  # 문장 생성 후 반환

    # thread
    def embedded_logic_thread(self):
        target_bname = "None"  # 찾아야 하는 비콘 이름 (default: None)
        data = {
            'root' : "None",
            'body' : "default"
        }
        while True:
            # 어떤 버튼이 눌렸는지 지속적으로 확인해야 함
            dict_button_data = self.__harward_ctrl.what_button_is_it()
            time.sleep(0.5)
            #print(dict_button_data)
            result =None

            # 과정 1. 가고자 하는 목적지 입력 및 경로 찾아 알림
            if self.__now_state == "PATH":
                result = self.__is_recv_queue_empty()
                if result:  # 들어있다면
                    data = self.__recv_deque()  # recv thread에 담겨있는 data 추출
                    #print(data)
                    if data['root'] == "PATH":  # data: ['root': destination, 'body': bus_number]
                        sentence_data = self.__make_sentence(data['body'])  # 입력받은 데이터로 사용자에게 알릴 문장 생성
                        filename=self.__text_to_wav(data=sentence_data)  # convert : txt > wav file
                        #self.__harward_ctrl.speaker_start(filename)  # speak
                        print(sentence_data)
                        self.__now_state = "BUS"  # 과정 2로 바꿔주기

            # 과정 2. 목적지까지 가는(== 내가 타야 할))버스 위치 파악
            if self.__now_state == "BUS":
                bname = self.__beacon_network.get_bus_beacon()
                
                if target_bname != "None":  # 즉, 비콘을 찾았다면
                    rssi = self.__beacon_network.get_rssi()  # RSSI 값 받기
                    self.__harward_ctrl.set_vib_distance(rssi)  # RSSI 거리에 따른 진동

                send_data = {"root" : "BUS", "body": bname}
                print("send data : ", send_data)
                self.__send_enque(send_data)

                result = self.__is_recv_queue_empty()
                if not result:  # 들어있다면
                    recv_data = self.__recv_deque()  # 뽑아내기
                    
                    if recv_data['body'] == bname:
                        target_bname = bname
                        self.__harward_ctrl.set_vib_flag[True]
                        # 이제 이 비콘만 찾으면 됨

            # button 1 function :: speak destination (== system input)
            if not dict_button_data['mic_button'][0]:
                self.__now_state = 'PATH'
                result = self.__harward_ctrl.mic_func_start()
                time.sleep(3)
                if not result:
                    continue
                self.__target_location = self.__wav_to_text()
                bname = self.__beacon_network.get_beacon()
                result_data = {
                    "root" : "PATH",
                    "bname" : bname,
                    "target" : self.__target_location}
                print(result_data)
                self.__send_enque(result_data)
            
            # button 2 function :: end system
            elif not dict_button_data['end_button'][0]:
                self.__now_state == "END"
                self.__harward_ctrl.set_vib_flag(False)
                break

            # button 3 function ??
            elif not dict_button_data['speak_button'][0] and self.__now_state != "BUS":  # 현 상태가 버스 찾기 전일 때(== 과정 1 단계)
                target_txt = "이 버스는 영남대 건너 정류장 입니다."
                filename = self.__text_to_wav(target_txt)
                time.sleep(1)
                print(target_txt)
                #self.__harward_ctrl.speaker_start(filename=filename)
            
            elif not dict_button_data['speak_button'][0] and self.__now_state == "BUS":  # 현 상태가 버스 찾는 중일 때(== 과정 2 단계)
                bname = self.__beacon_network.get_bus_beacon()
                target_txt = f"이 버스는 {bname}번 버스입니다"
                filename = self.__text_to_wav(target_txt)
                time.sleep(1)
                print(target_txt)
                #self.__harward_ctrl.speaker_start(filename=filename)

    # convert :: text > wav file
    def __text_to_wav(self, data):
        tts = gTTS(text=data, lang='ko', slow=False)  # 텍스트를 TTS 객체로 변환
        filename = "./temp/audio.wav"  # 임시 오디오 파일 이름
        tts.save(filename)  # 오디오 파일로 저장
        return filename
    
    # convert :: wav file > text
    #def __wav_to_text(self):
        #file_name = f"./temp/sample.wav"  # 바꿀 wav file
        #wr = Wav_Recognizer()
        #location = wr.recognizing_file(file_name)  # wav file 분석
        #return location
    
    def __wav_to_text(self):
        data = open("./temp/sample.wav", "rb") # STT를 진행하고자 하는 음성 파일

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
        dict_data = json.loads(response.text)
        text_data = dict_data['text']

        result = self.__extract_location(text_data)

        return result

    def __extract_location(self, sentence:str):
        sentence = sentence.replace(" ", "")

        # "으로" 또는 "에"가 포함된 부분을 추출
        match = re.search(r'(.+?)(으로|에)', sentence)
        
        if match:
            result = match.group(1).strip()
            print("target : ", result)
            return result
        else:
            return None


    # 이거 어케 하더라
    def button_thread(self):
        button_list = []
        while True:
            button_list = [GPIO.input(MIC_BUTTON), 
                           GPIO.input(END_BUTTON),
                           GPIO.input(SPEAK_BUTTON)]
            self.__harward_ctrl.button_pressed(button_list)
    
"""
# WAV 파일 분석기
class Wav_Recognizer:
    def __init__(self):
        self.__recognizer = sr.Recognizer()
    
    # 분석기
    def recognizing_file(self, file_path = "./temp/"):
        # 음성 파일 열기
        with sr.AudioFile(file_path) as source:
            audio = self.__recognizer.record(source, duration= 120)
        
        # text로 변환 
        text = self.__recognizer.recognize_google(audio_data=audio, language='ko-KR')
        location_result = self.__extract_location(text) 
        
        # 목적지 반환
        return location_result
    
    # 문장에서 핵심 경로 추출
    def __extract_location(self, sentence):
        # "으로" 또는 "에"가 포함된 부분을 추출
        match = re.search(r'(.+?)(으로|에)', sentence)
        
        if match:
            result = match.group(1).strip()
            return result
        else:
            return None
"""


