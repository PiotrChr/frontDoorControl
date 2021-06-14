from src.lib.messaging import dbMessenger
from src.lib.db import db as libdb


class PromptMessenger(dbMessenger.DbMessenger):
    MESSAGE_INFO = 'TEXT'
    MESSAGE_WARNING = 'WARNING'
    MESSAGE_ERROR = 'ERROR'
    MESSAGE_CLOSE = 'CLOSE'

    CONTEXT_PROMPT = 1  # 'PROMPT'

    def __init__(self,
                 db: libdb.Db):
        super().__init__(db)
