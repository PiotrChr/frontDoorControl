import speech_recognition as sr
import threading
from src.lib.voiceControl import voiceControl


class SpeechRecognition:
    TIMEOUT = 5
    PHRASE_TIME_LIMIT = 5

    def __init__(self, speech_recognition_handler: voiceControl.VoiceControl):
        self.recognizer = sr.Recognizer()
        self.handler = speech_recognition_handler

        self.stopped = False
        self.t = None

    def start(self):
        self.stopped = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True,
        )
        self.t.start()

    def stop(self):
        self.stopped = True

    def recognize(self, audio):
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            if self.handler.error_handler:
                self.handler.error_handler(
                    "Google Speech Recognition could not understand audio"
                )
        except sr.RequestError as e:
            if self.handler.error_handler:
                self.handler.error_handler(
                    "Could not request results from Google Speech Recognition service; {0}".format(e)
                )

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=self.TIMEOUT,
                    phrase_time_limit=self.PHRASE_TIME_LIMIT,
                )
            except sr.WaitTimeoutError:
                if self.handler.idle_handler:
                    self.handler.idle_handler()

        return audio

    def worker(self):
        while True and not self.stopped:
            audio = self.listen()
            recognized_text = self.recognize(audio)
            if not self.handler.handle(recognized_text):
                self.stopped = True
