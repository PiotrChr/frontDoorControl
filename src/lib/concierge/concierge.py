import threading

from src.lib.db import db as libdb
from src.lib.sound import mic_client as libmc, speaker_client as libsc
from src.lib.leds import leds as libleds
from src.lib.speechRecognition import speechRecognition
from src.lib.doorOpener import door_opener as libdooropener
from src.lib.screen import screen as libscreen
from src.service import accelerometerController, lightController, motionController
from src.lib.concierge import helpers as libhelpers
from src.service import buttonController
from src.lib.messaging import promptMessanger, promptMessage
from . import state
import subprocess
from settings import settings


class Concierge:
    MESSAGE_PROMPT_SCRIPT = 'messagePrompt.py'

    def __init__(
            self,
            db: libdb.Db,
            mic_client: libmc.MicClient,
            speaker_client: libsc.SpeakerClient,
            leds: libleds.Leds,
            event: threading.Event,
            acc: accelerometerController.AccelerometerController,
            door_opener: libdooropener.DoorOpener,
            motion: motionController.MotionController,
            light: lightController.LightController,
            speech: speechRecognition.SpeechRecognition,
            buttons: buttonController.ButtonController,
            screen: libscreen.Screen,
            prompt_messenger: promptMessanger.PromptMessenger,
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
        self.prompt_messenger = prompt_messenger
        self.state = state.State()
        self.event = event

    def init(self):
        self.setup_voice_control()
        self.leds.red_off()
        self.leds.white_off()
        self.screen.screen_off()
        self.setup_button_handlers()
        self.wait_for_action()

        self.event.wait(1)

    def start_sensors(self):
        self.motion.start()
        self.light.start()
        # self.acc.start()

    def setup_handlers(self):
        self.motion.set_handlers(lambda l: self.db.save_light(l))
        self.light.set_handlers(lambda: self.db.save_motion())
        self.acc.set_handlers(lambda x, y, z: self.db.save_acc(x, y, z, None, None, None))

    def send_text_message(self, text, style=promptMessanger.PromptMessenger.MESSAGE_INFO):
        self.prompt_messenger.send_message(promptMessage.PromptMessage(
            promptMessanger.PromptMessenger.MESSAGE_INFO,
            text,
            style
        ), promptMessanger.PromptMessenger.CONTEXT_PROMPT)

    def setup_voice_control(self):
        self.speech.handler.add_main_handler(
            lambda text: self.prompt_main_handler(text)
        )

        self.speech.handler.add_idle_handler(
            lambda: self.handle_idle_command
        )

        self.speech.handler.add_error_handler(
            lambda error: self.handle_command_error(error)
        )

        self.speech.handler.add_command(
            name="OpenDoor",
            regex_identifiers=[
                "open door"
            ],
            handler=lambda: self.open_door() or True
        )

        self.speech.handler.add_command(
            name="Greet",
            regex_identifiers=[
                "hello"
            ],
            handler=lambda: self.greet() or True
        )

        self.speech.handler.add_command(
            name="Greet",
            regex_identifiers=[
                "blink"
            ],
            handler=lambda: self.blink() or True
        )

        self.speech.handler.add_not_recognized_command(lambda: self.handle_not_recognized())

    def greet(self):
        print("Hello!")

    def blink(self):
        self.send_text_message(";)")
        self.leds.white_on()
        self.event.wait(0.5)
        self.leds.white_off()
        self.event.wait(0.5)
        self.leds.white_on()
        self.event.wait(0.5)
        self.leds.white_off()
        self.event.wait(1)
        self.wait_and_close()

    def prompt_main_handler(self, text):
        self.send_text_message("Cmd " + text)
        self.event.wait(1)

    def handle_command_error(self, error):
        self.send_text_message(error, promptMessanger.PromptMessenger.MESSAGE_ERROR)
        self.wait_and_close()

    def handle_idle_command(self):
        self.send_text_message("...?", promptMessanger.PromptMessenger.MESSAGE_WARNING)
        self.wait_and_close()

    def wait_and_close(self):
        self.event.wait(2)
        self.prompt_messenger.send_message(
            promptMessage.PromptMessage(promptMessanger.PromptMessenger.MESSAGE_CLOSE),
            promptMessanger.PromptMessenger.CONTEXT_PROMPT
        )
        self.screen.screen_off()
        self.state.screen = False

    def handle_not_recognized(self):
        self.send_text_message("I don't know what you mean.", promptMessanger.PromptMessenger.MESSAGE_WARNING)
        self.event.wait(4)
        self.wait_and_close()

    def handle_idle_press_red(self):
        if not self.state.screen:
            self.start_prompt_and_wait()
            self.send_text_message("How can I help?")

            self.listen_for_command()
        else:
            self.wait_and_close()

    def handle_idle_press_black(self):
        print("Black pressed")

    def setup_button_handlers(self):
        self.buttons.set_handler(lambda red, black: red and self.handle_idle_press_red())

    def wait_for_action(self):
        self.buttons.start()

    def listen_for_command(self):
        print("listen for command")
        self.speech.start()

    def start_prompt_and_wait(self):
        subprocess.Popen(['python3', settings['root_dir'] + self.MESSAGE_PROMPT_SCRIPT])
        self.event.wait(1)
        self.screen.screen_on()
        self.state.screen = True
        self.event.wait(4)

    def open_door(self):
        self.send_text_message("Opening")
        self.door_opener.open_door()
        self.event.wait(2)
        self.send_text_message("Opened")
        self.event.wait(1)
        self.send_text_message("Welcome home")
        self.event.wait(2)
        self.wait_and_close()


