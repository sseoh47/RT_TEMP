# import time
# import pygame    

# def text_to_speech():
#     try:
#         pygame.init()
#         # 볼륨 설정 (최대 1.0)
#         pygame.mixer.music.set_volume(1.0)
#         print("동기화체크")
#         pygame.mixer.music.load("/home/hyelim/RT_TEMP/client/test.wav")
#         #play
#         pygame.mixer.music.play()
#         print("*")
#         #끝까지 재생할때까지 기다린다.
#         while pygame.mixer.music.get_busy() == True:
#             continue

#     except Exception as e:
#         print(f"Error in text_to_speech: {e}")

# text_to_speech()

import vlc

file_path = "/home/hyelim/RT_TEMP/client/test.wav"  # 여기에 음원 파일의 절대 경로를 입력합니다.
player = vlc.MediaPlayer(file_path)
print("실행")
player.play()

# 재생이 끝날 때까지 대기
while player.is_playing():
    pass
