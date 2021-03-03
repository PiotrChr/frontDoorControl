from webstream import WebStream
import threading
from flask import Response
from flask import Flask
from flask import jsonify
from flask import render_template
from lib.motionsensor import motionsensor
import argparse

stream = WebStream()
app = Flask(__name__)


def motion_off():
    print("off")


def motion_on():
    print("on")


sensor = motionsensor.MotionSensor(
    off_handler=motion_off,
    on_handler=motion_on
)

sensor.start()


@app.route("/")
def index():
    return render_template("index.html")


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


def create_thread():
    thread = threading.Thread(target=stream.detect_motion, args=(
        args["frame_count"],))

    thread.daemon = True
    return thread


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

stream.stop()
