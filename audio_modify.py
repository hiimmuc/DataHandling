from pydub import AudioSegment
from pydub.playback import play
import glob
import pydub

pydub.AudioSegment.converter = r'C:\Users\phuongnam-d\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin\ffmpeg.exe'

files = glob.glob("mp3_files\SteffanNeural\\*.mp3")
for f in files:
    song = AudioSegment.from_mp3(f)

    # boost volume by 6dB
    louder_song = song + 6

    # save louder song
    louder_song.export(f, format='mp3')

files = glob.glob("wav_files\SteffanNeural\\*.wav")
for f in files:
    song = AudioSegment.from_wav(f)

    # boost volume by 6dB
    louder_song = song + 6

    # save louder song
    louder_song.export(f, format='wav')
