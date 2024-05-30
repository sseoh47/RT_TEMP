import pyaudio
import wave
from threading import Thread
import RPi.GPIO as GPIO
import pygame
import time
import numpy as np

# 진동 울리는 거리값
DIST_THRESHOLD = 4500
WARN_THRESHOLD = 2500
DANG_THRESHOLD = 1200
STOP_THRESHOLD = 500

VIB_PIN = 17
VIB_CYCLE = 2

BUTTON_PIN = 2

class 마이크임:
    def __init__(self) -> None:
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.WAVE_OUTPUT_FILENAME = r'sample.wav'
        self.frames = []

    def mic_record_on(self, button_state):
        try:
            frames = []

            p = pyaudio.PyAudio()

            stream = p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

            print('음성녹음 시작')

            while not button_state[0]:  # recording이 True인 동안 계속 녹음
                data = stream.read(self.CHUNK, exception_on_overflow = False) #overflow 해결위해 추가
                frames.append(data)

            print('음성녹음 완료')

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
        except :
            print("음성이 녹음 되다맘")
            return False
        return True


class HardwareCtrlClass:
    def __init__(self) -> None:
        self.__mic_button = [True]
        self.__end_button = [True]
        self.__speak_button = [True]
        self.__mic = 마이크임()
        self.__vib = Vibrater()
        self.__distance = [DIST_THRESHOLD]
        self.__vib_flag = [False]
        thread = Thread(target = self.__vib.give_vib_feedback,
                        args=(self.__distance, self.__vib_flag))
        self.__make_button()

    def set_vib_distance(self, distance):
        self.__distance = distance

    def set_vib_flag(self, state):
        self.__vib_flag[0] = state
    
    def button_pressed(self, button):
        self.__mic_button[0] = button

    def __make_button(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def speaker_start(self, filename):
        pygame.init()
        time.sleep(0.1)
        print("audio start : ", filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        return

    def what_button_is_it(self):
        dict_button_data= {
            "mic_button" : self.__mic_button,
            "end_button" : self.__end_button,
            "speak_button" : self.__speak_button,
        }
        return dict_button_data

    def mic_func_start(self):
        result = self.__mic.mic_record_on()
        return result



class Vibrater:
    def __init__(self, info):
        #GPIO.setmode(GPIO.BCM)
        GPIO.setup(VIB_PIN, GPIO.OUT)
        self.info = info
        # 진동 사이클
        self.cycle = VIB_CYCLE #초
    
    # 진동 사이클 제공
    def give_vib_feedback(self, distances = [DIST_THRESHOLD+1], flag = [False]):
        end_time=0
        while True:
            if not flag[0]:
                time.sleep(1)
            else:
            #distance=self.__find_min_dist(distances=distances)
                if(self.__check_distance(distances[0])):
                    now_time=time.time()
                    if(now_time-end_time>self.cycle):
                        GPIO.output(VIB_PIN,True)
                        time.sleep(0.3)
                        end_time=time.time()
                        GPIO.output(VIB_PIN,False)
            
    # 진동 사이클 지정
    def __check_distance(self, distance):
        if distance <= DIST_THRESHOLD and distance >= WARN_THRESHOLD:
            self.cycle = 3
        elif distance <= WARN_THRESHOLD and distance >= DANG_THRESHOLD:
            self.cycle = 1.5
        elif distance <= DANG_THRESHOLD and distance >= STOP_THRESHOLD:
            self.cycle = 0.5
        elif distance <= STOP_THRESHOLD:
            self.cycle = 0
        else:
            # 거리가 임계거리보다 크다면 False를 반환
            return False
        # 거리가 임계거리보다 작다면 True를 반환
        return True