import time
import pygame    

def text_to_speech():
        try:
            pygame.init()
            
            # WAV 파일을 재생하려면 pygame.mixer.Sound 사용
            sound = pygame.mixer.Sound('./test.wav')
            sound.play()
            print("*")
            
            # 재생 시간 동안 대기
            time.sleep(sound.get_length())
            
            # pygame 종료
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in text_to_speech: {e}")

text_to_speech()
