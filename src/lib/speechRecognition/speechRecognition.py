import speech_recognition as sr
import threading
from src.lib.voiceControl import voiceControl


class SpeechRecognition:
    TIMEOUT = 5
    PHRASE_TIME_LIMIT = 5

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.last_recognized_text = None

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

    def listen_and_recognize(self):
        audio = self.listen()
        self.last_recognized_text = self.recognize(audio)

        return self.last_recognized_text
