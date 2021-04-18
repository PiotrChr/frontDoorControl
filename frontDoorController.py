from lib.motionsensor import motionsensor
from lib.lightsensor import lightsensor
from lib.accelerometer import accelerometer
from lib.leds import leds
from lib.screen import screen
from lib.db import db
from lib.status import status

from datetime import datetime
from dateutil.parser import parse


class FrontDoorController:
    def __init__(self):
        self.motion_sensor = motionsensor.MotionSensor(
            off_handler=self.motion_off,
            on_handler=self.motion_on
        )

        self.light_sensor = lightsensor.LightSensor(
            sensor_handler=self.light_handler
        )

        self.acc = accelerometer.Accelerometer(
            sensor_handler=self.acc_handler
        )

        self.leds = leds.Leds()
        self.screen = screen.Screen()
        self.status = status.Status()

        self.db = db.Db()

        self.init()

    def init(self):
        self.db.setup()
        self.leds.red_off()
        self.leds.white_off()
        self.screen.screen_off()

    def start_all(self):
        self.motion_sensor.start()
        self.light_sensor.start()
        # self.acc.start()

    def motion_off(self):
        pass

    def motion_on(self):
        self.db.save_motion()

    def acc_handler(self, x, y, z):
        self.db.save_acc(x, y, z, None, None, None)

    def light_handler(self, light_level):
        self.db.save_light(light_level)

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

    def is_date(self, string, fuzzy=False):
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def clear_db(self, table, stop):
        if stop is not None and not self.is_date(stop):
            raise Exception('Can\'t read the date.')

        if table not in db.Db.TABLES:
            raise Exception('Table %s not found. Can\'t delete.' % (table,))

        self.db.clear_db_up_to_date(table, stop)

    def read_status(self):
        return {
            'fs_total': self.status.get_total_space(),
            'fs_used': self.status.get_used_space(),
            'db_size': self.status.get_db_size()
        }
