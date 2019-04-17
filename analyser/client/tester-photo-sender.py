import sys
sys.path.append("./analyser/")

import os
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
    payload = {'distance' : dist, 'fileName': os.path.basename(img_file.name)}


    files = {'media': img_file.read()}
    # requests.post(server['url'], files=files)
    #send the data to server
    try:
        response = requests.post(server['url'], files = {'file': open(picturePath, 'rb')}, params=payload)

    except:
        print("Error sending message to server: " + server['url'])
        exit()
    img_file.close()

    print(response.text)
    time.sleep(0.2)


