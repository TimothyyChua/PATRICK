import os
import threading
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
import numpy as np

import json

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config('Config.JSON')

#file_path = 'sound.wav'  # Change this to your file path

class AudioPlayer:
    def __init__(self, file_path, play_duration, volume=1.0):
        self.file_path = file_path
        self.play_duration = play_duration
        self.volume = volume  # Volume level (0.0 to 1.0)
        self.thread = None
        self.stop_event = threading.Event()

    def _play_wav_file(self):
        data, sample_rate = sf.read(self.file_path)
        num_samples = int(self.play_duration * sample_rate)
        if num_samples > len(data):
            num_samples = len(data)
        data_to_play = data[:num_samples]
        data_to_play = data_to_play * self.volume  # Adjust volume
        sd.play(data_to_play, sample_rate)
        while sd.get_stream().active and not self.stop_event.is_set():
            sd.sleep(100)

    def _play_mp3_file(self):
        audio = AudioSegment.from_mp3(self.file_path)
        play_duration_ms = self.play_duration * 1000
        if play_duration_ms > len(audio):
            play_duration_ms = len(audio)
        audio_to_play = audio[:play_duration_ms]
        audio_to_play = audio_to_play + (self.volume * 100 - 100)  # Adjust volume (pydub uses dB)
        data = np.array(audio_to_play.get_array_of_samples())
        if audio_to_play.channels == 2:
            data = data.reshape((-1, 2))
        sd.play(data, audio.frame_rate)
        while sd.get_stream().active and not self.stop_event.is_set():
            sd.sleep(100)

    def _play_audio(self):
        self.stop_event.clear()
        file_extension = os.path.splitext(self.file_path)[1].lower()
        if file_extension == '.wav':
            self._play_wav_file()
        elif file_extension == '.mp3':
            self._play_mp3_file()
        else:
            print(f"Unsupported file format: {file_extension}")

    def play(self):
        self.thread = threading.Thread(target=self._play_audio)
        self.thread.start()

    def is_playing(self):
        return self.thread.is_alive() if self.thread else False

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            sd.stop()
            self.thread.join()

    def set_volume(self, volume):
        self.volume = volumeead(target=self._play_audio)
        self.thread.start()

    def is_playing(self):
        return self.thread.is_alive() if self.thread else False

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            sd.stop()
            self.thread.join()

    def wait_until_finished(self):
        if self.thread:
            self.thread.join()



