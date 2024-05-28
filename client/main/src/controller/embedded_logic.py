from queue import Queue
from controller.beacon_network import BeaconNetwork
from controller.hardware_ctrl import HardwareCtrlClass
from threading import Thread
import RPi.GPIO as GPIO

from gtts import gTTS
import speech_recognition as sr
import re  # String 분석용도 
import time

class EmbeddedLogic:
    def __init__(self) -> None:
        self.__recv_queue=Queue()
        self.__send_queue=Queue()
        self.__now_state = "default"  # PATH or BUS or default
        self.__beacon_network = BeaconNetwork
        self.__harward_ctrl = HardwareCtrlClass
        self.__target_location = ""
        
    def is_send_queue_empty(self)->bool:
        result=self.__send_queue.empty()
        return result

    def __is_recv_queue_empty(self)->bool:
        result=self.__recv_queue.empty()
        return result

    def recv_enque(self, dict_data:dict):
        print(dict_data)
        self.__recv_queue.put(dict_data)

    def __send_enque(self, dict_data:dict):
        print(dict_data)
        self.__send_queue.put(dict_data)

    def send_deque(self)->dict:
        dict_data = self.__send_queue.get()
        print(dict_data)
        return dict_data

    def __recv_deque(self)->dict:
        dict_data = self.__recv_queue.get()
        print(dict_data)
        return dict_data
    
    def __make_sentence(self, data):
                # 버스를 찾지 못했을 때
        if data == "None":
            return {"result": f"{self.__target_location}로 갈 수 있는 버스는 없습니다. 죄송합니다."}
        
        # 버스 찾았을 때 Dict 형태로 반환 데이터 준비
        sentence_data = f"{self.__target_location}으로 가기 위해 {data}"
        sentence_data = sentence_data + "번 버스를 타야 합니다. 감사합니다."
        return sentence_data

    
    def embedded_logic_thread(self):
        target_bname = "None"
        
        while True:
            dict_button_data = self.__harward_ctrl.what_button_is_it()

            if self.__now_state == "PATH":
                result = self.__is_recv_queue_empty()
                if result:
                    data = self.__recv_deque()
                    if data['root'] == "PATH":
                        sentence_data = self.__make_sentence(data['body'])
                        filename=self.__text_to_wav(data=sentence_data)
                        self.__harward_ctrl.speaker_start(filename)
                        self.__now_state = "BUS"

            if self.__now_state == "BUS":
                bname = self.__beacon_network.get_bus_beacon()
                if target_bname != "None":
                    rssi = self.__beacon_network.get_rssi()
                    self.__harward_ctrl.set_vib_distance(rssi)


                send_data = {"root" : "BUS", "body": bname}
                self.__send_enque(send_data)

                result = self.__is_recv_queue_empty()
                if not result:
                    recv_data = self.__recv_deque()
                    if recv_data['body'] == bname:
                        target_bname = bname
                        self.__harward_ctrl.set_vib_flag[True]
                        # 이제 이 비콘만 찾으면 됨

            if not dict_button_data['mic_button'][0]:
                self.__now_state = 'PATH'
                result = self.__harward_ctrl.mic_func_start()
                time.sleep(1)
                if not result:
                    continue
                self.__target_location = self.__wav_to_text()
                bname = self.__beacon_network.get_beacon()
                result_data = {
                    "root" : "PATH",
                    "bname" : bname,
                    "target" : self.__target_location}
                self.__send_enque(result_data)
            
            elif dict_button_data['end_button'][0]:
                self.__now_state == "END"
                self.__harward_ctrl.set_vib_flag(False)

            elif dict_button_data['end_button'][0] and self.__now_state != "BUS":
                bname = self.__beacon_network.get_beacon()               
                target_txt = "이 버스는 영남대 건너 정류장 입니다."
                filename = self.__text_to_wav(target_txt)
                self.__harward_ctrl.speaker_start(filename=filename)
            
            elif dict_button_data['end_button'][0] and self.__now_state == "BUS":
                target_txt = f"이 버스는 {bname}번 버스입니다"
                filename = self.__text_to_wav(target_txt)
                self.__harward_ctrl.speaker_start(filename=filename)


    def __text_to_wav(self, data):
        tts = gTTS(text=data, lang='ko', slow=False)  # 텍스트를 TTS 객체로 변환
        filename = "./temp/audio.wav"  # 임시 오디오 파일 이름
        tts.save(filename)  # 오디오 파일로 저장
        return filename
    
    def __wav_to_text(self):
        file_name = f"./temp/sample.wav"
        wr = Wav_Recognizer()
        location = wr.recognizing_file(file_name)
        return location

    # 이거 어케 하더라
    def button_thread(self):
        while True:
            button_state = GPIO.input(2)
            self.__harward_ctrl.button_pressed(button_state)
    

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

