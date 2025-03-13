from multiprocessing import Process, Queue
from Camera import Cam
from processing import Processor
import torch
import cv2
import schedule
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

class Recall():
    def __init__(self):
        self.frameQueue = Queue()
        self.cam = Cam(self.frameQueue)
        self.processor = Processor()
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s")
        self.updateBackground = True
        schedule.every(5).minutes.do(self.everyFive)
        print("done Initial")

    def run(self):
        while True:
            
            if not self.frameQueue.empty():
                # print("infer1")
                frame = self.frameQueue.get()
                self.infer(frame)
                # Run background
                if self.updateBackground:
                    self.updateBackground = False
                    self.obtainBackground(frame)
                    

    def infer(self, frame):
        results = self.model(frame)
        r = results.xyxy[0].numpy()
        # print("infer")
        for row in r:
            # print(row)
            xmin, ymin, xmax, ymax, confidence, cls = row
            xmin, ymin, xmax, ymax, cls = int(xmin), int(ymin), int(xmax), int(ymax), int(cls)

            # Check Phone
            if classNames[int(cls)] == "cell phone" and confidence > 0.6:
                
                x = xmin+(xmax-xmin)/2
                y = ymin+(ymax-ymin)/2
                
                drawnFrame= cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 255), 3)

                # Push into Processor
                self.processor.detectionsQueue.put((14, x, y, drawnFrame))

    def obtainBackground(self, frame):
        surroundings = []
        results = self.model(frame)
        r = results.xyxy[0].numpy()
        # print("infer")
        for row in r:
            # print(row)
            xmin, ymin, xmax, ymax, confidence, cls = row
            xmin, ymin, xmax, ymax, cls = int(xmin), int(ymin), int(xmax), int(ymax), int(cls)
            if classNames[cls] != "person" and classNames[cls] != "cell phone" and confidence > 0.6:
                x = xmin+(xmax-xmin)/2
                y = ymin+(ymax-ymin)/2
                surroundings.append((x, y, classNames[cls]))

        self.processor.surroundingsQueue.put(surroundings)

    def onTimer(self):
        # raise background flag
        self.updateBackground = True

        # tell the processor to ask for updates

if __name__ == "__main__":
    app = Recall()
    app.run()