import shutil
from src.lib.db import db
import os


class Status:

    def __init__(self):
        self.total = None
        self.used = None
        self.free = None
        self.db_file_name = None

        self.refresh()

    def refresh(self):
        total, used, free = shutil.disk_usage("/")

        self.total = total // (2**30)
        self.used = used // (2**30)
        self.free = free // (2**30)
        self.db_file_name = db.Db.DB_FILE

    # IN MB
    def get_db_size(self):
        return os.path.getsize(self.db_file_name) / 1048576

    # IN GB
    def get_total_space(self):
        return self.total

    # IN GB
    def get_used_space(self):
        return self.used
