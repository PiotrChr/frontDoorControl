from src.lib.db import db as libdb
from src.lib.messaging import message


class DbMessenger:
    def __init__(
            self,
            db: libdb.Db
    ):
        self.db = db

    def send_message(self, _message: message.Message, context):
        self.db.save_message(_message.toJSON(), context)
