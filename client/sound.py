from gtts import gTTS
import pygame
import os, wave
import time
#from playsound import playsound

class SOUND:
    def __init__(self):
        print("start sound")

    def text_to_speech(self, text, lang='en'):
        try:
            tts = gTTS(text=text, lang=lang, slow=False)  # 텍스트를 TTS 객체로 변환
            filename = "./station.mp3"  # 임시 오디오 파일 이름
            tts.save(filename)  # 오디오 파일로 저장

            pygame.init()
            os.environ["SDL_AUDIODRIVER"]="pulseaudio"
            pygame.mixer.init(devicename='hw:1,0')

            sound=pygame.mixer.Sound(filename)
            sound.play(
            pygame.time.wait(int(sound.get_length()*1000))
            )            
            # os.remove(filename)  # 재생 후 오디오 파일 삭제
        except Exception as e:
            print(f"Error in text_to_speech_pyaudio: {e}")

    def play_wav_file(self, wav_path):
        # 절대 경로 확인
        abs_path = os.path.abspath(wav_path)
        if os.path.exists(abs_path):
            print("*")
            playsound(abs_path)
        else:
            print(f"파일을 찾을 수 없습니다: {abs_path}")