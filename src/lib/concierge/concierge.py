from src.lib.db import db as libdb
from src.lib.sound import mic_client as libmc, speaker_client as libsc
from src.lib.leds import leds as libleds
from src.lib.speechRecognition import speechRecognition
from src.lib.doorOpener import door_opener as libdooropener
from src.lib.screen import screen as libscreen
from src.service import accelerometerController, lightController, motionController
from src.lib.concierge import helpers as libhelpers
from src.service import buttonController
from src.lib.view import messagePrompt
from . import state
import time


class Concierge:
    def __init__(
            self,
            db: libdb.Db,
            mic_client: libmc.MicClient,
            speaker_client: libsc.SpeakerClient,
            leds: libleds.Leds,
            acc: accelerometerController.AccelerometerController,
            door_opener: libdooropener.DoorOpener,
            motion: motionController.MotionController,
            light: lightController.LightController,
            speech: speechRecognition.SpeechRecognition,
            buttons: buttonController.ButtonController,
            screen: libscreen.Screen,
            prompt: messagePrompt.MessagePrompt,
            helpers: libhelpers.Helpers,

    ) -> None:
        self.db = db
        self.acc = acc
        self.mic_client = mic_client
        self.speaker_client = speaker_client
        self.leds = leds
        self.door_opener = door_opener
        self.motion = motion
        self.light = light
        self.speech = speech
        self.screen = screen
        self.helpers = helpers
        self.buttons = buttons
        self.prompt = prompt
        self.state = state.State()

    def init(self):
        self.setup_voice_control()
        self.leds.red_off()
        self.leds.white_off()
        self.screen.screen_off()
        self.setup_button_handlers()
        self.wait_for_action()

        time.sleep(1)
        self.test()

    def start_sensors(self):
        self.motion.start()
        self.light.start()
        # self.acc.start()

    def setup_handlers(self):
        self.motion.set_handlers(lambda l: self.db.save_light(l))
        self.light.set_handlers(lambda: self.db.save_motion())
        self.acc.set_handlers(lambda x, y, z: self.db.save_acc(x, y, z, None, None, None))

    def setup_voice_control(self):
        self.speech.handler.add_command(
            name="OpenDoor",
            regex_identifiers=[
                "open door"
            ],
            handler=lambda p: self.open_door() or True
        )

        self.speech.handler.add_command(
            name="Greet",
            regex_identifiers=[
                "Hello"
            ],
            handler=lambda p: self.greet() or True
        )

        self.speech.handler.add_not_recognized_command(lambda: print("Not recognized"))

    def greet(self):
        print("Hello!")

    def handle_idle_press_red(self):
        self.listen_for_command()

    def handle_idle_press_black(self):
        print("Black pressed")

    def setup_button_handlers(self):
        self.buttons.set_handler(lambda red, black: red and self.handle_idle_press_red())

    def wait_for_action(self):
        self.buttons.start()

    def listen_for_command(self):
        self.speech.start()

    def test(self):
        self.prompt.start()
        time.sleep(2)
        self.prompt.dispatch_message("Opening")
        self.prompt.dispatch_message("Opened")
        self.prompt.stop()

    def open_door(self):
        self.prompt.start()
        time.sleep(2)
        self.prompt.dispatch_message("Opening")
        self.door_opener.open_door()
        time.sleep(1)
        self.prompt.dispatch_message("Opened")
        self.prompt.stop()


