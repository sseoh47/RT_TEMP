import time
import pygame    

def text_to_speech():
        try:
            pygame.init()
            pygame.mixer.music.load("./test.wav")
            #play
            pygame.mixer.music.play()
            #끝까지 재생할때까지 기다린다.
            while pygame.mixer.music.get_busy() == True:
                continue

        except Exception as e:
            print(f"Error in text_to_speech: {e}")

text_to_speech()
