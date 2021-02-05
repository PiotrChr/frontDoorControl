from webstream import WebStream
import threading
from flask import Response
from flask import Flask
from flask import jsonify
from flask import render_template
import argparse

stream = WebStream()
app = Flask(__name__)


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
        t.start()

    return jsonify(stream_running=stream.running())


@app.route("/feed_stop")
def feed_stop():
    if stream.running():
        stream.stop()

    return jsonify(stream_running=stream.running())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    t = threading.Thread(target=stream.detect_motion, args=(
        args["frame_count"],))
    t.daemon = True

    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

stream.stop()
