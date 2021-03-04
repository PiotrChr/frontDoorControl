from lib.motionsensor import motionsensor
from lib.lightsensor import lightsensor


class FrontDoorController:
    def __init__(self):
        self.motion_sensor = motionsensor.MotionSensor(
            off_handler=self.motion_off,
            on_handler=self.motion_on
        )

        self.light_sensor = lightsensor.LightSensor(
            sensor_handler=self.light_handler
        )

    def start_all(self):
        self.motion_sensor.start()
        self.light_sensor.start()

    def motion_off(self):
        print("off")

    def motion_on(self):
        print("on")

    def light_handler(self, light_level):
        print(light_level)
