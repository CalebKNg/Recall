import cv2
from picamera2 import Picamera2
import math
import torch
import time
# ~ from picamera import PiCamera
# ~ from picamera import PiRGBArray


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
    results = model(frame, stream=True)

        # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            # print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            # print("Class name -->", classNames[cls])
            



            # object details
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.putText(frame, box.cls, org, font, fontScale, color, thickness)



    cv2.imshow('Camera', frame)
    
    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# ~ # Release the capture and writer objects
# ~ cam.release()
# ~ out.release()
cv2.destroyAllWindows()
