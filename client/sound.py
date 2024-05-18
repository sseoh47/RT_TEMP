from gtts import gTTS
from playsound import playsound
import os

class SOUND:
    def __init__(self):
        print("start sound")

    def text_to_speech(text, lang='en'):
        try:
            tts = gTTS(text=text, lang=lang, slow=False)  # 텍스트를 TTS 객체로 변환
            filename = "station.wav"  # 임시 오디오 파일 이름
            tts.save(filename)  # 오디오 파일로 저장
            playsound(filename)  # 저장된 오디오 파일 재생
            os.remove(filename)  # 재생 후 오디오 파일 삭제
        except Exception as e:
            print(f"Error in text_to_speech_pyaudio: {e}")
