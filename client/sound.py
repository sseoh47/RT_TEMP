from gtts import gTTS
import pygame
import os
from ps import*

class SOUND:
    def __init__(self):
        print("start sound")

    def text_to_speech(self, text, lang='en'):
        try:
            tts = gTTS(text=text, lang=lang, slow=False)  # 텍스트를 TTS 객체로 변환
            filename = "./station.wav"  # 임시 오디오 파일 이름
            tts.save(filename)  # 오디오 파일로 저장
            pygame.mixer.init()
            sound = pygame.mixer.Sound(filename)
            sound.play()
            #os.remove(filename)  # 재생 후 오디오 파일 삭제
        except Exception as e:
            print(f"Error in text_to_speech_pyaudio: {e}")
