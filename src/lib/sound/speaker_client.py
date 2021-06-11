from src.lib.sound import sound


class SpeakerClient(sound.Sound):
    CHUNK = 1024
    DEVICE_INDEX = 1
    RECORD_SECONDS = 4
    CHANNELS = 1

    def __init__(self):
        super().__init__(
            self.DEVICE_INDEX,
            self.CHUNK
        )

    def readFromFile(self):
        pass

    def readFromSocket(self, host):
        pass
