import cv2
from multiprocessing import Process, Queue
from picamera2 import MappedArray, Picamera2

class Cam():
    def __init__(self, Q):
        picam2 = Picamera2()
        picam2.video_configuration.controls.FrameRate = 25.0
        picam2.post_callback = self.fillArray
        self.Q = Q
        picam2.start()

    def fillArray(self, request):
        with MappedArray(request, "main") as m:
            self.Q.put(m.array)