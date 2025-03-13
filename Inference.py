import cv2
from picamera2 import Picamera2
import math
import torch
import time
# ~ from picamera import PiCamera
# ~ from picamera import PiRGBArray
# object classes
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
# classNames = ["wallet", "airpod", "cell Phone"]
# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# Open the default camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()
# Bit of a delay for camera
time.sleep(0.1)



while True:
    # ~ ret, frame = cam.read()
    # Display the captured frame
    frame = camera.capture_array()

    # inference
    results = model(frame)
    r = results.xyxy[0].numpy()

    for row in r:
        xmin, ymin, xmax, ymax, confidence, cls = row
        
        xmin, ymin, xmax, ymax, cls = int(xmin), int(ymin), int(xmax), int(ymax), int(cls)
        
    # boxes = results.boxes

    # for box in boxes:
    #     # bounding box
    #     x1, y1, x2, y2 = box.xyxy[0]
    #     x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

    #     # put box in cam

    #     # confidence
    #     confidence = math.ceil((box.conf[0]*100))/100
    #     # print("Confidence --->",confidence)

    #     # class name
    #     cls = int(box.cls[0])
    #     # print("Class name -->", classNames[cls])
        



        # object details
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 255), 3)
        org = [xmin, ymin]
        org2 = [xmin-200, ymin-200 ]
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)
        # cv2.putText(frame, str(confidence), org, font, fontScale, color, thickness)



    time.sleep(0.05)
    cv2.imshow('Camera', frame)
    
    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# ~ # Release the capture and writer objects
# ~ cam.release()
# ~ out.release()
cv2.destroyAllWindows()
