from src.lib.voiceControl import command as libcommand
from pprint import pprint
import threading


class VoiceControl:
    NOT_RECOGNIZED_COMMAND = "NOT_RECOGNIZED"

    def __init__(self, event: threading.Event):
        self.main_handler = None
        self.idle_handler = None
        self.error_handler = None
        self.handlers = []
        self.not_recognized = None
        self.event = event

    def add_command(self, name, regex_identifiers, has_params=False, param_filters=None, handler=None):
        self.handlers.append(
            libcommand.Command(
                name=name,
                regex_identifiers=regex_identifiers,
                has_params=has_params,
                param_filters=param_filters,
                handler=handler
            )
        )

    def add_main_handler(self, handler=None):
        self.main_handler = handler

    def add_idle_handler(self, handler=None):
        self.idle_handler = handler

    def add_error_handler(self, handler=None):
        self.error_handler = handler

    def add_not_recognized_command(self, handler=None):
        self.not_recognized = libcommand.Command(
            name=self.NOT_RECOGNIZED_COMMAND,
            handler=handler
        )

    def handle(self, text):
        if self.main_handler:
            self.main_handler(text)

        command = self.get_command_by_text(text)
        if not command:
            command = self.not_recognized

        command.handle()

    def get_command_by_text(self, text):
        for command in self.handlers:
            if command.match_and_prepare(text):
                return command

        return None
