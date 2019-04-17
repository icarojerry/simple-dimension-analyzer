import sys
sys.path.append("./analyser/")

import time
import cv2
import random
import requests
from parameters.config import client
from parameters.config import server

def takePicture():
    return client['dir_img'] + '/example_01.png'

#capture the distance from sensor
def distance():
    return 11.0

def waitingTriggerButton():
    return

def setup():
    pass

if __name__ == '__main__':
    setup()

    while True:
        waitingTriggerButton()

        #GPIO.output(24, True)
        dist = distance()
        picturePath = takePicture()

        try:
            img_file = open(picturePath, 'rb')
        except FileNotFoundError:
            print('Image: ' + picturePath + ' not found...')
            exit()

        #prepare parameters to send request
        files = {'media': img_file}
        headers = {'Content-Type' : 'image/jpeg'}
        payload = {'distance' : dist, 'fileName': picturePath}

        #send the data to server
        try:
            response = requests.post(server['url'], data=img_file.read(), headers=headers, verify=False, params=payload)
        except:
            print("Error sending message to server: " + server['url'])
            exit()
        img_file.close()

        print(response)

        print ("Measured Distance = %.1f cm" % dist)
        print ("Server response" % response)
        time.sleep(0.2)

