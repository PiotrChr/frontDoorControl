from src.lib.view import window
import tkinter
from pprint import pprint
from src.lib.messaging import promptMessanger


class MessageWindow(window.Window):
    UPDATE_MESSAGE_EVENT = '<<UpdateMessage>>'

    def __init__(self):
        super().__init__()

    def init(self, title="Message"):
        super().init(title)
        self.set_fullscreen()

        self.main_frame.message_label = self.create_main_message_label(self.main_frame)
        self.main_frame.message_label.pack(anchor=self.tkinter.CENTER, expand=True)

    def create_main_message_label(self, container):
        message_label = tkinter.Label(
            container,
            text="Text",
            font=('Arial', 25)
        )

        message_label.pack()

        return message_label

    def update_message(self, message, style=None):
        print('style', style)

        if style == promptMessanger.PromptMessenger.MESSAGE_WARNING:
            fg = '#eb8034'
        elif style == promptMessanger.PromptMessenger.MESSAGE_ERROR:
            fg = '#ff0000'
        else:
            fg = '#000'

        self.main_frame.message_label.config(text=message, fg=fg)
