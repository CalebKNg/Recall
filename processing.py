import requests
from multiprocessing import Process, Queue
import heapq
from collections import deque
import config

class Object:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.x = 0
        self.y = 0
        self.locHistory = deque()
        self.isMoving = True
        self.lastLocationImage = ""


# This class processes and communicates
class Processor():
    def __init__(self):
        self.detectionsQueue = Queue()
        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        while True:
            pass

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
    # print("obtain")
    # print(headers)
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