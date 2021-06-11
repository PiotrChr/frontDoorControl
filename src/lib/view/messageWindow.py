from src.lib.view import window
import tkinter


class MessageWindow(window.Window):
    def __init__(self):
        super().__init__("Message")

        self.main_frame.message_label = self.create_main_message_label(self)
        self.main_frame.message_label.pack()

    def init(self):
        self.main_frame.message_label = self.create_main_message_label(self)

    def create_main_message_label(self, container):
        message_label = tkinter.Label(
            container,
            text=""
        )

        message_label.pack()

        return message_label

    def send_message(self, message):
        self.main_frame.message_label.config(text=message)
