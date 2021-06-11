import sqlite3 as sl
from datetime import datetime


class Db:
    DB_FILE = 'resources/db/main.db'

    TABLE_ACC = 'acc'
    TABLE_MOTION = 'motion'
    TABLE_LIGHT = 'light'

    COLUMN_ACC_X = 'acc_x'
    COLUMN_ACC_Y = 'acc_y'
    COLUMN_ACC_Z = 'acc_z'

    COLUMN_GYRO_X = 'gyro_x'
    COLUMN_GYRO_Y = 'gyro_y'
    COLUMN_GYRO_Z = 'gyro_z'

    COLUMN_LIGHT_LEVEL = 'light_level'

    COLUMN_CREATED_AT = 'created_at'
    COLUMN_ID = 'id'

    TABLES = [TABLE_ACC, TABLE_MOTION, TABLE_LIGHT]

    BATCH_SIZE_SMALL = 3
    BATCH_SIZE = 10

    def __init__(self):
        self.connection = sl.connect(Db.DB_FILE, check_same_thread=False)
        self.connection.row_factory = self.dict_factory

        self.light_batch = []
        self.acc_batch = []
        self.motion_batch = []

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def setup(self):
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS acc (
                        id INTEGER PRIMARY KEY,
                        acc_x INT NULL,
                        acc_y INT NULL,
                        acc_z INT NULL,
                        gyro_x INT NULL,
                        gyro_y INT NULL,
                        gyro_z INT NULL,
                        created_at DATETIME NOT NULL    
                    )
                """)

                self.connection.execute("""
                    CREATE INDEX IF NOT EXISTS idx_acc_created_at
                    ON acc (created_at)
                """)

                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS motion (
                        id INTEGER PRIMARY KEY,
                        created_at DATETIME NOT NULL    
                    )
                """)

                self.connection.execute("""
                    CREATE INDEX IF NOT EXISTS idx_motion_created_at
                    ON acc (created_at)
                """)

                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS light (
                        id INTEGER PRIMARY KEY,
                        light_level INT NOT NULL,
                        created_at DATETIME NOT NULL    
                    )
                """)

                self.connection.execute("""
                    CREATE INDEX IF NOT EXISTS idx_light_created_at
                    ON acc (created_at)
                """)
        except Exception as e:
            print('Exception', e)

    def save_acc(self, acc_x=None, acc_y=None, acc_z=None, gyro_x=None, gyro_y=None, gyro_z=None):
        if not self.acc_batch:
            self.acc_batch = []

        self.acc_batch.append((None, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, datetime.now()))

        if len(self.acc_batch) < self.BATCH_SIZE:
            return

        try:
            with self.connection:
                self.connection.executemany("""
                    INSERT INTO acc
                    values (?,?,?,?,?,?,?,?)
                """, self.acc_batch)
        except Exception as e:
            print('Exception', e)

        self.acc_batch = []

    def save_light(self, light_level=None):
        if not self.light_batch:
            self.light_batch = []

        self.light_batch.append((None, light_level, datetime.now()))

        if len(self.light_batch) < self.BATCH_SIZE_SMALL:
            return

        try:
            with self.connection:
                self.connection.executemany("""
                    INSERT INTO light
                    values (?,?,?)
                """, self.light_batch)
        except Exception as e:
            print('Exception', e)

        self.light_batch = []

    def save_motion(self):
        try:
            with self.connection:
                created_at = datetime.now()

                self.connection.execute("""
                    INSERT INTO motion
                    values (?,?)
                """, (None, created_at))
        except Exception as e:
            print('Exception', e)

    def get_acc_by_date(self, start, stop):
        return self.get_by_date('acc', start, stop)

    def get_motion_by_date(self, start, stop):
        return self.get_by_date('motion', start, stop)

    def get_light_by_date(self, start, stop):
        return self.get_by_date('light', start, stop)

    def get_by_date(self, table, start, stop):
        with self.connection:
            cur = self.connection.cursor()

            print(start, stop)
            cur.execute("""
                SELECT * FROM %s
                WHERE
                    created_at BETWEEN ? and ?
                ORDER BY
                    created_at ASC 
            """ % (table,), (start, stop))

            return cur.fetchall()

    def clear_all(self):
        self.clear_db_up_to_date('acc')
        self.clear_db_up_to_date('motion')
        self.clear_db_up_to_date('light')

    def clear_db_up_to_date(self, table, stop=None):
        with self.connection:
            if stop:
                self.connection.execute("""
                    DELETE FROM %s
                    WHERE
                        created_at <= ? 
                """ % (table,), (stop,))
            else:
                self.connection.execute("DELETE FROM %s" % (table,))

        pass

    def clear_acc(self):
        self.clear_db_up_to_date('acc')

    def clear_motion(self):
        self.clear_db_up_to_date('motion')

    def clear_light(self):
        self.clear_db_up_to_date('light')

    def clear_light_up_to_date(self, stop):
        self.clear_db_up_to_date('light', stop)

    def clear_motion_up_to_date(self, stop):
        self.clear_db_up_to_date('motion', stop)

    def clear_acc_up_to_date(self, stop):
        self.clear_db_up_to_date('acc', stop)
