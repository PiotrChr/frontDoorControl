from src.lib.db import db as libdb


class DayPasswordRepository:
    def __init__(
            self,
            db: libdb.Db
    ):
        self.db = db

    def get_current_password(self):
        return self.db.get_current_password()
