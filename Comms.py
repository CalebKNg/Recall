import requests
import config
from multiprocessing import Process, Queue


class Comms():
    def __init__(self, token):
        self.requestsToSend = Queue()
        self.bearerToken = token
        
        self.process = Process(target=self.run)
        self.process.start()

    def sendUpdate(self, id, name, image, description):
        url = "https://fydp-backend-production.up.railway.app/ObjectTracking/" + str(id) + "/"
        headers = {"Content-Type": "application/json", "Authorization":"Bearer " + self.bearerToken}

        data = {
            "name": name,
            "location_image": image,
            "location_description": description
        }

        response = requests.patch(url, json=data, headers=headers)
        print(response.status_code)   

    def run(self):
        while True:
            if not self.requestsToSend.empty():
                det = self.requestsToSend.get() 
                id, name, image, description = det
                self.sendUpdate(id, name, image, description)

    def terminate(self):
            self.process.terminate()
            self.process.join()
