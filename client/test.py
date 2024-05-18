import time
import pygame    

def text_to_speech():
        try:
            # tts = gTTS(text=text, lang=lang, slow=False)  # 텍스트를 TTS 객체로 변환
            filename = "./sample.wav"  # 임시 오디오 파일 이름
            # tts.save(filename)  # 오디오 파일로 저장
            pygame.init()
            time.sleep(1)
            print("*")
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            # os.remove(filename)  # 재생 후 오디오 파일 삭제
        except Exception as e:
            print(f"Error in text_to_speech: {e}")

text_to_speech()
