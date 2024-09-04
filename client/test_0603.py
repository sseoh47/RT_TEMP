import wave, os
import pygame

pygame.init()
os.environ["SDL_AUDIODRIVER"] = "pulseaudio"
# 오디오 잭(bcm2835 Headphones)을 사용하도록 설정
pygame.mixer.init(devicename='Headphones')

wav_file = './test.wav'
sound = pygame.mixer.Sound(wav_file)
sound.play()
pygame.time.wait(int(sound.get_length() * 1000))
