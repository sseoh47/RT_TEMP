import time
import pygame    

def text_to_speech():
    try:
        pygame.init()
        # 볼륨 설정 (최대 1.0)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.load("/home/hyelim/RT_TEMP/client/test.wav")
        #play
        pygame.mixer.music.play()
        print("*")
        #끝까지 재생할때까지 기다린다.
        while pygame.mixer.music.get_busy() == True:
            continue

    except Exception as e:
        print(f"Error in text_to_speech: {e}")

text_to_speech()
