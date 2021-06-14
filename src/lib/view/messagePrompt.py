from src.lib.view import messageWindow as libwindow
import threading


class MessagePrompt:
    def __init__(
            self,
            message_window: libwindow.MessageWindow
    ) -> None:
        self.message_window = message_window
        self.t = None
        self.stopped = False
        self.handler = None

    def start(self):
        self.stopped = False
        self.t = threading.Thread(
            target=self.worker,
            daemon=True
        )
        self.t.start()

    def dispatch_message(self, message):
        self.message_window.update_message(message)

    def stop(self):
        self.stopped = True
        self.message_window.close()

    def set_handlers(self, handler=None):
        self.handler = handler

    def worker(self):
        self.message_window.init()
        self.message_window.start()
