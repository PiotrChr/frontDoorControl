from dependency_injector import containers, providers

from src.lib.db import db
from src.lib.speechRecognition import speechRecognition
from src.lib.lightsensor import lightsensor
from src.lib.concierge import concierge
from src.lib.leds import leds
from src.lib.motionsensor import motionsensor
from src.lib.screen import screen
from src.lib.sound import mic_client, speaker_client
from src.lib.status import status
from src.lib.voiceAnalysis import voiceAnalysis
from src.lib.voiceControl import voiceControl
from src.lib.accelerometer import accelerometer
from src.service import accelerometerController
from src.service import lightController
from src.service import motionController
from src.service import gpio
from src import frontDoorController
from src.lib.concierge import helpers
from src.lib.doorOpener import door_opener
from src.lib.buttons import buttons as libbuttons
from src.service import buttonController
from src.lib.view import messageWindow, messagePrompt


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(
        db.Db
    )

    # Services
    gpio = providers.Singleton(
        gpio.Gpio
    )

    voice_control = providers.Factory(
        voiceControl.VoiceControl
    )

    speech_recognition = providers.Factory(
        speechRecognition.SpeechRecognition,
        speech_recognition_handler=voice_control
    )

    acc_sensor = providers.Factory(
        accelerometer.Accelerometer
    )

    acc_controller = providers.Factory(
        accelerometerController.AccelerometerController,
        accelerometer_sensor=acc_sensor
    )

    light_sensor = providers.Factory(
        lightsensor.LightSensor
    )

    light_controller = providers.Factory(
        lightController.LightController,
        light_sensor=light_sensor
    )

    leds = providers.Factory(
        leds.Leds,
        gpio=gpio
    )

    motion_sensor = providers.Factory(
        motionsensor.MotionSensor,
        gpio=gpio
    )

    motion_controller = providers.Factory(
        motionController.MotionController,
        motion_sensor=motion_sensor
    )

    screen = providers.Factory(
        screen.Screen,
        gpio=gpio
    )

    mic_client = providers.Factory(
        mic_client.MicClient
    )

    speaker_client = providers.Factory(
        speaker_client.SpeakerClient
    )

    status = providers.Factory(
        status.Status
    )

    helpers = providers.Factory(
        helpers.Helpers
    )

    buttons = providers.Factory(
        libbuttons.Buttons,
        gpio=gpio
    )

    buttons_controller = providers.Factory(
        buttonController.ButtonController,
        buttons=buttons
    )

    door_opener = providers.Factory(
        door_opener.DoorOpener
    )

    voice_analysis = providers.Factory(
        voiceAnalysis.VoiceAnalysis
    )

    message_window = providers.Factory(
        messageWindow.MessageWindow
    )

    message_prompt = providers.Factory(
        messagePrompt.MessagePrompt,
        message_window=message_window
    )

    concierge = providers.Factory(
        concierge.Concierge,
        db=db,
        helpers=helpers,
        door_opener=door_opener,
        speech=speech_recognition,
        mic_client=mic_client,
        speaker_client=speaker_client,
        buttons=buttons_controller,
        leds=leds,
        acc=acc_controller,
        motion=motion_controller,
        light=light_controller,
        prompt=message_prompt,
        screen=screen
    )

    front_door_controller = providers.Factory(
        frontDoorController.FrontDoorController,
        db=db,
        concierge=concierge,
        status=status
    )

