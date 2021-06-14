from src.lib.messaging import message, promptMessanger


class PromptMessage(message.Message):
    def __init__(self, name, text=None, style=None):
        super().__init__(promptMessanger.PromptMessenger.CONTEXT_PROMPT, name)

        self.text = text
        self.style = style
