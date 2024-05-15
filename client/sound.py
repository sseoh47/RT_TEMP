from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io

# 텍스트를 오디오로 변환하고 재생하는 함수
def text_to_speech_pyaudio(text, lang='ko'):
    tts = gTTS(text=text, lang=lang)  # gTTS를 사용하여 텍스트를 오디오로 변환
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)  # 오디오 데이터를 바이트 스트림으로 저장
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp, format="mp3")  # 오디오 스트림을 AudioSegment 객체로 변환
    play(audio)  # 오디오 재생

# 사용 예시
