import json

from src.lib.view import messageWindow
from src.lib.db import db
from src.lib.messaging import message as libmessage, promptMessanger
from pprint import pprint


class MessagePrompt:
    MESSENGER_CONTEXT = promptMessanger.PromptMessenger.CONTEXT_PROMPT

    def __init__(self):
        self.message_window = messageWindow.MessageWindow()
        self.message_window.init("Message Prompt")

        self.db = db.Db()

    def start(self):
        self.message_window.master.after(2000, self.worker())
        self.message_window.start()

    def worker(self):
        _id, message = self.get_message()
        if message:
            self.handle_message(message, _id)

        self.message_window.master.after(200, lambda: self.worker())

    def get_message(self):
        try:
            message = self.db.get_last_message_by_context(self.MESSENGER_CONTEXT)
            if message:
                return message['id'], json.loads(message['message'])
        except Exception as e:
            print(e)

        return None, None

    def update_message(self, message):
        self.message_window.update_message(message)

    def handle_message(self, message, id):
        self.db.set_message_as_handled(id)
        function = None
        handled = True

        if message['name'] == promptMessanger.PromptMessenger.MESSAGE_INFO:
            function = lambda: self.message_window.update_message(
                message['text'], message['style']
            )
        elif message['name'] == promptMessanger.PromptMessenger.MESSAGE_CLOSE:
            function = lambda: self.stop()
        else:
            handled = False

        if handled:
            self.db.set_message_as_handled(id)
            function()

    def stop(self):
        self.message_window.close()


prompt = MessagePrompt()
prompt.start()
