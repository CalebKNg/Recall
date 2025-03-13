from multiprocessing import Process, Queue
from Camera import Cam
import torch

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
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s")

    def run(self):
        while True:
            if not self.frameQueue.empty():
                frame = self.frameQueue.get()
                self.infer(frame)

    def infer(self, frame):
        results = self.model(frame)
        r = results.xyxy[0].numpy()

        for row in r:
            xmin, ymin, xmax, ymax, confidence, cls = row
            if classNames[cls] == "person" and confidence > 0.6:
                xmin, ymin, xmax, ymax, cls = int(xmin), int(ymin), int(xmax), int(ymax), int(cls)
                x = xmin+(xmax-xmin)/2
                y = ymin+(ymax-ymin)/2
                print(str(x)+str(y))

    



# Run the model on the current frame, obtain the image
def controlCam():
    pass

# Process the image. If the objects have stopped moving, send infomation to the endpoint
def process():
    pass

# Check endpoint for new items to be tracked (probably  not)
def update():
    pass

if __name__ == "__main__":
    app = Recall()
    app.run()