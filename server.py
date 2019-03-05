import zmq
import time
import numpy as np

from picamera.array import PiRGBArray
from picamera import PiCamera

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5555")

# camera setup
camera = PiCamera()
camera.resolution = (160,120)
camera.framerate = 30
# tuning
camera.exposure_mode = 'sports'
camera.color_effects = (128,128)

rawCapture = PiRGBArray(camera, size=(160,120))
stream = camera.capture_continuous(rawCapture,
            format="rgb", use_video_port=True)

for f in stream:
    # grab the frame from the stream and clear the stream in
    # preparation for the next frame
    arr = np.array(f.array, dtype='uint8')
    rawCapture.truncate(0)
    socket.send(np.fmax.reduce(arr,axis=2))
