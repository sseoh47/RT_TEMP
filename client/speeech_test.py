import speech_recognition as sr
#import sys #-- 텍스트 저장시 사용

r = sr.Recognizer()
kr_audio = sr.AudioFile('./test.wav')

with kr_audio as source:
    audio = r.record(source)

#sys.stdout = open('news_out.txt', 'w') #-- 텍스트 저장시 사용
print(r.recognize_google_cloud(audio, language='ko-KR'))