# import the necessary packages
from imagesearch.motion_detection.singlemotiondetector import SingleMotionDetector
from imutils.video import VideoStream
import threading
import datetime
import imutils
import time

import cv2


class WebStream:
    def __init__(self):
        self.outputFrame = None
        self.lock = threading.Lock()
        self.vs = VideoStream(usePiCamera=1)
        self.is_started = False

    def running(self):
        return self.is_started

    def init(self):
        self.vs = VideoStream(usePiCamera=1)

    def start(self):
        if not self.vs:
            self.init()

        self.vs.start()
        time.sleep(2.0)
        self.is_started = True

    def stop(self):
        self.vs.stop()
        time.sleep(0.5)
        self.is_started = False
        time.sleep(0.5)
        self.vs = None

    def detect_motion(self, frame_count):
        # initialize the motion detector and the total number of frames
        # read thus far
        md = SingleMotionDetector(accumWeight=0.1)
        total = 0
        # loop over frames from the video stream
        while True and self.is_started:
            if not self.is_started:
                break
            # read the next frame from the video stream, resize it,
            # convert the frame to grayscale, and blur it
            frame = self.vs.read()
            frame = imutils.resize(frame, width=400)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            # grab the current timestamp and draw it on the frame
            timestamp = datetime.datetime.now()
            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            # if the total number of frames has reached a sufficient
            # number to construct a reasonable background model, then
            # continue to process the frame
            if total > frame_count:
                # detect motion in the image
                motion = md.detect(gray)
                # check to see if motion was found in the frame
                if motion is not None:
                    # unpack the tuple and draw the box surrounding the
                    # "motion area" on the output frame
                    (thresh, (minX, minY, maxX, maxY)) = motion
                    cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                                  (0, 0, 255), 2)

            # update the background model and increment the total number
            # of frames read thus far
            md.update(gray)
            total += 1
            # acquire the lock, set the output frame, and release the
            # lock
            with self.lock:
                self.outputFrame = frame.copy()

    def generate(self):
        # loop over frames from the output stream
        while True and self.is_started:
            if not self.is_started:
                break
            # wait until the lock is acquired
            with self.lock:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if self.outputFrame is None:
                    continue
                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", self.outputFrame)
                # ensure the frame was successfully encoded
                if not flag:
                    continue
            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')
