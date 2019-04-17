import sys
sys.path.append("./analyser/")

import RPi.GPIO as GPIO
import time
import cv2
import pygame, sys
import pygame.camera
import random
import requests
from parameters.config import client
from parameters.config import server


def takePicture():
    pygame.init()
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video0", (640,480))

    print ("Taking a shot:")
    cam.start()
    image = cam.get_image()
    cam.stop()

    timestamp = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    filename = "%s/%s.jpg" % (server['dir_img'], timestamp)
    print ("saving into %s" % filename)

    pygame.image.save(image, filename)

    return filename



#capture the distance from sensor
def distance():
    client['speed_of_sound']
    max_delta_t = client['max_distance'] / client['speed_of_sound']
    

    # Gera um pulso de 10ms em TRIG.
    # Essa ação vai resultar na transmissão de ondas ultrassônicas pelo
    # transmissor do módulo sonar.
    GPIO.output(client.pin['trigger'], True)
    time.sleep(0.00001)
    GPIO.output(client.pin['trigger'], False)
 
    # Atualiza a variável start_t enquanto ECHO está em nível lógico baixo.
    # Quando ECHO trocar de estado, start_t manterá seu valor, marcando
    # o momento da borda de subida de ECHO. Este é o momento em que as ondas
    # sonoras acabaram de ser enviadas pelo transmissor.
    while GPIO.input(ECHO) == 0:
      start_t = time.time()
 
    # Atualiza a variável end_t enquando ECHO está em alto. Quando ECHO
    # voltar ao nível baixo, end_t vai manter seu valor, marcando o tempo
    # da borda de descida de ECHO, ou o momento em que as ondas refletidas
    # por um objeto foram captadas pelo receptor. Caso o intervalo de tempo
    # seja maior que max_delta_t, o loop de espera também será interrompido.
    while GPIO.input(ECHO) == 1 and time.time() - start_t < max_delta_t:
      end_t = time.time()
 
    # Se a diferença entre end_t e start_t estiver dentro dos limites impostos,
    # atualizamos a variável delta_t e calculamos a distância até um obstáculo.
    # Caso o valor de delta_t não esteja nos limites determinados definimos a
    # distância como -1, sinalizando uma medida mal-sucedida.
    if end_t - start_t < max_delta_t:
        delta_t = end_t - start_t
        distance = 100*(0.5 * delta_t * speed_of_sound)
    else:
        distance = -1

    return round(distance, 2)



def waitingTriggerButton():
    goOut = false
    print(client['pin'].button)
    while GPIO.input(client['pin'].button):
        while not GPIO.input(client['pin'].button):
            goOut = true;

        if goOut:
            time.sleep(0.5)
            break

    print('Button Pressed...')
    return

def setup():
    GPIO.setmode(GPIO.BCM)

    #Button to GPIO23
    GPIO.setup(client.pin['button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Define TRIG como saída digital
    GPIO.setup(client.pin['trigger'], GPIO.OUT)
    # Define ECHO como entrada digital
    GPIO.setup(client.pin['echo'], GPIO.IN)

if __name__ == '__main__':
    try:
        setup()
        while True:
            waitingTriggerButton()
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

            print ("Measured Distance = %.1f cm" % dist)
            print ("Server response" % response)
            time.sleep(0.2)

    except:
        GPIO.cleanup()