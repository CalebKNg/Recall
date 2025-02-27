import cv2
from picamera2 import Picamera2
import time
# ~ from picamera import PiCamera
# ~ from picamera import PiRGBArray

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
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# ~ # Release the capture and writer objects
# ~ cam.release()
# ~ out.release()
cv2.destroyAllWindows()
