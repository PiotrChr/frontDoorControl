from lib.concierge import concierge as libconcierge
from lib.db import db as libdb
from lib.status import status as libstatus
from datetime import datetime
from di import container
from dependency_injector.wiring import inject, Provide
from pprint import pprint


class FrontDoorController:

    def __init__(
            self,
            db: libdb.Db,
            concierge:  libconcierge.Concierge,
            status: libstatus.Status
    ) -> None:
        self.concierge = concierge
        self.status = status

        self.db = db

    def init(self):
        self.db.setup()
        self.concierge.init()

    def read_motion_by_date(self, start=None, stop=None):
        if not stop:
            stop = datetime.now()

        if not start:
            start = datetime.min

        return self.db.get_motion_by_date(start, stop)

    def read_acc_by_date(self, start=None, stop=None):
        if not stop:
            stop = datetime.now()

        if not start:
            start = datetime.min

        return self.db.get_acc_by_date(start, stop)

    def read_light_by_date(self, start=None, stop=None):
        if not stop:
            stop = datetime.now()

        if not start:
            start = datetime.min

        return self.db.get_light_by_date(start, stop)

    def clear_db_all(self):
        self.db.clear_all()

    def clear_db(self, table, stop):
        if stop is not None and not self.concierge.helpers.is_date(stop):
            raise Exception('Can\'t read the date.')

        if table not in libdb.Db.TABLES:
            raise Exception('Table %s not found. Can\'t delete.' % (table,))

        self.db.clear_db_up_to_date(table, stop)

    def read_status(self):
        return {
            'fs_total': self.status.get_total_space(),
            'fs_used': self.status.get_used_space(),
            'db_size': self.status.get_db_size()
        }
