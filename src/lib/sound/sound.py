import pyaudio
import time


class Sound:
    FORMAT = pyaudio.paInt16
    RATE = 44100
    CHANNELS = 1

    def __init__(self, dev_index, chunk):
        # self.pyaudio = pyaudio.PyAudio()
        self.pyaudio = None
        self.stream = None
        self.dev_index = dev_index
        self.chunk = chunk

    def write(self):
        pass

    def read(self):
        data = self.stream.read(self.chunk)

        return data

    def open_stream(self):
        self.stream = self.pyaudio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=self.dev_index
        )

    def pause(self):
        self.stream.stop_stream()

    def close_stream(self):
        while self.stream.is_active():
            time.sleep(0.1)

        self.stream.close()
        self.stream.terminate()
