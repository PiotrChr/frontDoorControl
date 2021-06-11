#!/usr/bin/python3

from webstream import WebStream
import threading
from flask import Response
from flask import Flask
from flask import jsonify
from flask import render_template
from src import frontDoorController
from src.lib.delivery.statsDecorator import decorate as stats_decorate
from src.di import container as dicontainer
from dependency_injector.wiring import inject, Provide
import sys
import argparse


@inject
def main(
        front_door_controller: frontDoorController.FrontDoorController = Provide[
            dicontainer.Container.front_door_controller
        ]
) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    stream = WebStream()

    app = Flask(__name__)
    app.container = container

    front_door_controller.init()

    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/door/<action>")
    def door(action=None):
        if action.find('open') != -1:
            front_door_controller.concierge.open_door()

            return jsonify({'status': 'Door Opened'})

        return jsonify({'status': 'No action performed'})

    @app.route("/maintenance/<action>/<value>")
    @app.route("/maintenance/<action>")
    def maintenance(action=None, value=None):
        if action.find('clear_') != -1:
            table = action.split('clear_')[1]
            front_door_controller.clear_db(table, value)

            return jsonify({'status': 'Table %s cleared' % (table,)})

        return jsonify({'status': 'No action performed'})

    @app.route("/status")
    def status():
        return jsonify(status=front_door_controller.read_status())

    @app.route("/read_motion/<start_date>/<end_date>")
    @app.route("/read_motion/<start_date>")
    @app.route("/read_motion")
    def read_motion(start_date=None, end_date=None):
        motion = stats_decorate(
            front_door_controller.read_motion_by_date(start_date, end_date),
            'motion'
        )

        return jsonify(motion)

    @app.route("/read_acc/<start_date>/<end_date>")
    @app.route("/read_acc/<start_date>")
    @app.route("/read_acc")
    def read_acc(start_date=None, end_date=None):
        acc = stats_decorate(
            front_door_controller.read_acc_by_date(start_date, end_date),
            'acc'
        )

        return jsonify(acc)

    @app.route("/read_light/<start_date>/<end_date>")
    @app.route("/read_light/<start_date>")
    @app.route("/read_light")
    def read_light(start_date=None, end_date=None):
        light = stats_decorate(
            front_door_controller.read_light_by_date(start_date, end_date),
            'light'
        )

        return jsonify(light)

    @app.route("/video_feed")
    def video_feed():
        return Response(stream.generate(),
                        mimetype="multipart/x-mixed-replace; boundary=frame")

    @app.route("/feed_start")
    def feed_start():
        if not stream.running():
            stream.start()
            t = create_thread()
            t.start()

        return jsonify(stream_running=stream.running())

    @app.route("/feed_status")
    def feed_status():
        return jsonify(stream_running=stream.running())

    @app.route("/feed_stop")
    def feed_stop():
        if stream.running():
            stream.stop()

        return jsonify(stream_running=stream.running())

    @app.route("/light_on")
    def light_on():
        front_door_controller.concierge.leds.white_on()

        return jsonify(light_on=True)

    @app.route("/light_off")
    def light_off():
        front_door_controller.concierge.leds.white_off()

        return jsonify(light_on=False)

    def create_thread():
        thread = threading.Thread(target=stream.detect_motion, args=(
            args["frame_count"],))

        thread.daemon = True
        return thread


if __name__ == '__main__':
    container = dicontainer.Container()
    container.wire(modules=[sys.modules[__name__]])

    main()

# stream.stop()
