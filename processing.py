import requests
from multiprocessing import Process, Queue
import heapq
from collections import deque
import config
import base64
import numpy as np
import cv2

class Object:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.x = 0
        self.y = 0
        self.locHistory = deque()
        self.isMoving = True
        self.lastLocationImage = ""

relational_words = [
        "the right of", "above", "to the left of", "below", 
    ]

# This class processes and communicates
class Processor():
    def __init__(self):
        # Constants
        self.historyLength = 60
        self.avgLength = 10
        self.sector_size = 360/90

        # Queues
        self.detectionsQueue = Queue()
        self.surroundingsQueue = Queue()

        # Tracked objects list
        self.trackedObjects = []
        # List of surrounding objects
        self.surroundings = []

        # Get Token
        self.bearerToken = self.obtainBearer()

        # Get Initial List
        self.obtainObjects()

        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        while True:
            
            if not self.detectionsQueue.empty():
                det = self.detectionsQueue.get()
                # unpack detection
                id, x, y, frame = det
                self.updateLocations(id, x, y, frame)

            # Update Surroundings
            if not self.surroundingsQueue.empty():
                
                surr = self.surroundingsQueue.get()
                self.surroundings = surr


    def updateLocations(self, id, x, y, frame):
        for item in self.trackedObjects:
            if item.id == id:
                print("Update Phone")
                # Grab average of the locHistory 
                xsum = 0
                ysum = 0
                for location in item.locHistory:
                    xsum += location[0]
                    ysum += location[1]
                xavg = xsum/len(item.locHistory)
                yavg = ysum/len(item.locHistory)

                # Grab average of the last 5 
                xrec = 0
                yrec = 0
                for i in range(self.avgLength):
                    xrec += item.locHistory[i][0]
                    yrec += item.locHistory[i][1]
                xrec = xrec/self.avgLength
                yrec = yrec/self.avgLength

                # euclidean distance
                dist = np.sqrt((xrec - xavg)**2 + (yrec - yavg)**2)
                print(dist)
                threshold = 0.01
                if item.isMoving:
                    if dist < threshold:
                        # stopped moving
                        print("stopped moving")
                        # print("Phone moved " + str(dist) + "pixels")
                        item.isMoving = False
                        output = self.toB64(frame)

                        pts = self.findKNearestPoints(x, y)
                        outputString = self.relationalString(x, y, pts)
                        print(outputString)
                        # make request
                        # self.sendUpdate(item.id, output, outputString)

                else:   # If not moving
                    if dist >= threshold:
                        print("started moving")
                        item.isMoving = True
                        # print("Phone is moving")

                # print(item.isMoving)
                # Update distance
                item.x = x
                item.y = y
                item.lastLocationImage = self.toB64(frame)

                # Update queue
                if(len(item.locHistory) > self.historyLength):
                    item.locHistory.pop()
                    item.locHistory.appendleft((x, y))
                else:
                    item.locHistory.appendleft((x, y))




    def obtainBearer(self):
            url = "https://fydp-backend-production.up.railway.app/api/auth/login/" 
            headers = {"Content-Type": "application/json"}
            data = config.data
            response = requests.post(url, json=data, headers=headers)
            # print(response.status_code)

            if (response.status_code == 200):
                # print(response.json()["access"])
                return response.json()["access"]
            
    def obtainObjects(self):
        # Ask for a list of objects
        url = "https://fydp-backend-production.up.railway.app/ObjectTracking/" 
        headers = {"Content-Type": "application/json", "Authorization":"Bearer " + self.bearerToken}

        response = requests.get(url, headers=headers)
        # print(response.status_code)
        if(response.status_code == 200):
            for item in response.json():
                id = item["id"]
                name = item["name"]
                ob = Object(id, name)
                for i in range(self.avgLength): 
                    ob.locHistory.append((0,0))
                self.trackedObjects.append(ob)
            # self.trackedObjects = response.json()   

    def sendUpdate(self, id, name, image, description):
        url = "fydp-backend-production.up.railway.app/ObjectTracking/" + str(id)
        headers = {"Content-Type": "application/json", "Authorization":"Bearer " + self.bearerToken}

        data = {
            "name": name,
            "location_image": image,
            "location_description": description
        }

        response = requests.patch(url, json=data, headers=headers)
        print(response.status_code)    

    def findKNearestPoints(self, x, y):
        k = 3
        heap = []
        for px, py, s in self.surroundings:
            distance = np.sqrt((px - x) ** 2 + (py - y) ** 2)
            heapq.heappush(heap, (distance, (px, py, s)))
        return [heapq.heappop(heap)[1] for _ in range(min(k, len(heap)))]

    def relationalString(self, x, y, points):
        string = "Check "
        for px, py, s in points:
            angle = int(self.angleBetween(x, y, px, py))
            # string = string + relational_words[int(360//angle)]
            string = string + relational_words[self.angle_to_direction_int(angle)]

            string = string + " " + s + ", "

        return string

    def angleBetween(self, x, y, x2, y2):
        xdiff = x2 - x
        ydiff = y2 - y
        return np.arctan(ydiff/xdiff)*180/np.pi
    
    def angle_to_direction_int(self, angle):
        if angle < 45 or angle > 315 or angle == 0 or angle == 360:
            return 0  # Right
        elif 45 <= angle < 135:
            return 1  # Up
        elif 135 <= angle < 225:
            return 2  # Left
        elif 225 <= angle < 315:
            return 3  # Down

    def toB64(self, img):
            _, buffer = cv2.imencode('.jpg', img)
            im_bytes = buffer.tobytes()
            b64 = base64.b64encode(im_bytes)
            return b64.decode("utf-8")
        


    def terminate(self):
            self.process.terminate()
            self.process.join()
