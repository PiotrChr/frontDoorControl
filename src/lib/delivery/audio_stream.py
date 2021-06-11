from src.lib.delivery.socket import socket
from settings import settings
import threading
import pickle
from src.lib.sound import mic_client


class AudioStream(socket.Socket):
    def __init__(self):
        super().__init__(settings['HOST'])
        self.stop = False
        self.t = None
        self.mic_client = mic_client.MicClient()

    def start(self):
        self.stop = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True,
            args=(
                self.handler,
                self.stop,
            )
        )
        self.t.start()

    def worker(self):
        self.mic_client.open_stream()

        while True and not self.stop:
            self.handler()

        self.mic_client.pause()
        self.mic_client.close_stream()

    def stop(self):
        self.stop = True

    def handler(self):
        i = 0
        frames = []

        while i < 20:
            data = self.mic_client.read()
            frames.append(data)
            i += 1

        self.connection.send(pickle.dumps(frames))
