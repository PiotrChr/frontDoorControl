import pyaudio
from src.lib.sound import sound


class MicClient(sound.Sound):
    CHUNK = 1024
    DEVICE_INDEX = 1
    RECORD_SECONDS = 4
    CHANNELS = 1

    def __init__(self):
        super().__init__(self.DEVICE_INDEX, self.CHUNK)

    def read(self):
        data = self.stream.read(self.CHUNK)

        return data
