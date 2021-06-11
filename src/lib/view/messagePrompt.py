from src.lib.view import messageWindow as libwindow
import threading


class MessagePrompt:
    def __init__(
            self,
            message_window: libwindow.MessageWindow
    ) -> None:
        self.message_window = message_window
        self.t = None
        self.stop = False
        self.handler = None
        self.new_message = None

    def start(self):
        self.stop = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True
        )
        self.t.start()

    def dispatch_message(self, message):
        self.new_message = message

    def stop(self):
        self.stop = True

    def set_handlers(self, handler=None):
        self.handler = handler

    def worker(self):
        self.message_window.start()

        if self.new_message:
            self.message_window.send_message(self.new_message)
            self.new_message = None

        if self.stop:
            self.message_window.close()
