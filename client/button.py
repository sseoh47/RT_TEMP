import pyaudio
import wave
import threading
import RPi.GPIO as GPIO

class BUTTON:
    CHUNK = 516
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = r'sample.wav'
    BUTTON_PIN = 2

    frames = []
    recording = False

    def Start_Recording(self):
        global frames
        frames = []

        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        print('음성녹음 시작')
        time.sleep(1)
        while self.recording:  # recording이 True인 동안 계속 녹음
            data = stream.read(self.CHUNK, exception_on_overflow = False) #overflow 해결위해 추가
            frames.append(data)
        time.sleep(1)

        print('음성녹음 완료')

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


    def record_dest(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        try:
            while True:
                button_state = GPIO.input(self.BUTTON_PIN)

                if button_state == False and not self.recording:  # 여기 수정
                    self.recording = True  # 여기 수정
                    thread = threading.Thread(target=self.Start_Recording)
                    thread.start()
                elif button_state == True and self.recording:  # 여기 수정
                    self.recording = False  # 여기 수정
                    thread.join()  # 녹음 스레드가 종료될 때까지 기다립니다.
                    break

        except KeyboardInterrupt:
            GPIO.cleanup()  # 프로그램 종료 시 GPIO 설정 초기화


import time
if __name__ =="__main__":
    b = BUTTON()
    thread = threading.Thread(target=b.record_dest)
    thread.start()
    time.sleep(3)
    b.Start_Recording()


