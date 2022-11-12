from src.lib.speechRecognition import speechRecognition
from src.lib.voiceControl import voiceControl


class VoiceControlManager:

    # TODO: Initialize everything here instead of concierge
    def __init__(
            self,
            voice_control: voiceControl.VoiceControl,
            speech_recognition: speechRecognition.SpeechRecognition
    ):
        self.stopped = False
        self.t = None
        self.voiceControl = voice_control
        self.speechRecognition = speech_recognition

    def authenticate(self):
        recognized_text = self.speechRecognition.listen_and_recognize()

    def start(self):
        self.stopped = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True,
        )
        self.t.start()

    def stop(self):
        self.stopped = True

    def worker(self):
        recognized_text = self.speechRecognition.listen_and_recognize()

        self.voiceControl.get_command_by_text()