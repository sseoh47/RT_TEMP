import time
import pygame    

def text_to_speech():
    try:
        import pygame

        pygame.mixer.init()
        sounda = pygame.mixer.Sound("/home/hyelim/RT_TEMP/client/test.wav")
        sounda.play()
        pygame.time.wait(int(sounda.get_length() * 1000))

    except Exception as e:
        print(f"Error in text_to_speech: {e}")

text_to_speech()
