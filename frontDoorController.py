from lib.motionsensor import motionsensor
from lib.lightsensor import lightsensor
from lib.leds import leds
from lib.screen import screen


class FrontDoorController:
    def __init__(self):
        self.motion_sensor = motionsensor.MotionSensor(
            off_handler=self.motion_off,
            on_handler=self.motion_on
        )

        self.light_sensor = lightsensor.LightSensor(
            sensor_handler=self.light_handler
        )
        self.leds = leds.Leds()
        self.screen = screen.Screen()

        self.init()

    def init(self):
        self.leds.red_off()
        self.leds.white_off()
        self.screen.screen_off()

    def start_all(self):
        self.motion_sensor.start()
        self.light_sensor.start()

    def motion_off(self):
        print("off")

    def motion_on(self):
        print("on")

    def light_handler(self, light_level):
        print(light_level)
