import json


class Message:
    def __init__(self, context, name):
        self.name = name
        self.context = context

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
