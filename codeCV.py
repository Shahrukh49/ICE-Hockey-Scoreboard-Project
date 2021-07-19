import pygame
import time
import cv2 as cv
import numpy as np
import os
import sys
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sensor1 = 21
sensor2 = 26
led1 = 23
led2 = 25

GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(sensor1,GPIO.IN)
GPIO.setup(sensor2,GPIO.IN)

def sensor1_call(channel):
    global led1, score1
    GPIO.output(led1, 1)
    score1 +=1
    pygame.mixer.music.load('New York Islanders 2020 Goal Horn (NYCB Live).mp3')
    pygame.mixer.music.play()
    os.system('omxplayer /home/pi/icehockey/2021video3.mov')
    GPIO.output(led1, 0)
    time.sleep(0.5)

def sensor2_call(channel):
    global led2, score2
    GPIO.output(led2, 1)
    score2 +=1
    pygame.mixer.music.load('New York Islanders Goal Horn History Ringtone.mp3')
    pygame.mixer.music.play()
    os.system('omxplayer /home/pi/icehockey/alltimevideo3.mov')
    GPIO.output(led2, 0)
    time.sleep(0.5)

GPIO.add_event_detect(sensor1, GPIO.FALLING, callback=sensor1_call, bouncetime=200)
GPIO.add_event_detect(sensor2, GPIO.FALLING, callback=sensor2_call, bouncetime=200)

pygame.init()

width, height = 1024,600
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('ICEHOCKEY LIVE')

clock = pygame.time.Clock()

image = pygame.image.load('nimg2.png')
image = pygame.transform.scale(image, (width, height))

# pygame.camera.init()
# cam = pygame.camera.Camera('/dev/video0',(1024,600))
# cam.start()

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
width2 = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height2 = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
print(width2, height2)

score1 = 0
score2 = 0

white = (255,255,255)

font = pygame.font.SysFont('Arial', 90)

#pygame.mixer.music.load('islesvideo.mp3')
#pygame.mixer.music.play()
os.system('omxplayer /home/pi/icehockey/islesvideo3.mov')


while True:
    gameDisplay.fill((0, 0, 0))
# 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #cam.stop()
            cap.release()
            pygame.quit()
            sys.exit()
        #print(event)
# 
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            x, y = pos
            #1207, 21 == 1260, 72
            if x >= width*0.943 and x <= width*0.9844 and y >= height*0.0292 and y <=height*0.1:
                cap.release()
                pygame.quit()
                sys.exit()
            if x >= width*0.065 and x <= width*0.108 and y >= height*0.732 and y <= height*0.8:
                if score1 > 0:
                    score1 -= 1

            if x >= width*0.898 and x <= width*0.941 and y >= height*0.732 and y <= height*0.7875:
                if score2 > 0:
                    score2 -= 1

            if x >= width*0.065 and x <= width*0.108 and y >= height*0.646 and y <= height*0.7153:
                score1 += 1

            if x >= width*0.898 and x <= width*0.941 and y >= height*0.646 and y <= height*0.7153:
                score2 += 1
# 
#     img = cam.get_image()
#     img = pygame.transform.flip(img, True, False)
#     gameDisplay.blit(img,(0,0))
# 
    ret, frame = cap.read()
    camera = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
# #
    camera=np.rot90(camera)
    camera = pygame.surfarray.make_surface(camera)
    gameDisplay.blit(camera, (0,0))
    gameDisplay.blit(image, (0,0))
# 
    text1 = font.render(str(score1), True, white)
    text2 = font.render(str(score2), True, white)
# 
# 
    gameDisplay.blit(text1, (width*0.3844, height*0.653))
    gameDisplay.blit(text2, (width*0.575, height*0.653))
# 
# ##    RECTANGLE TESTING -------------
# ##    pygame.draw.rect(gameDisplay, white, pygame.Rect(width*0.943, height*0.0292, 60, 60))
# ##    pygame.draw.rect(gameDisplay, white, pygame.Rect(width*0.065, height*0.732, 60, 60))
# ##    pygame.draw.rect(gameDisplay, white, pygame.Rect(width*0.898, height*0.732, 60, 60))
# 
    pygame.display.flip()
    clock.tick(60)


print("out")
#cam.stop()
cap.release()
pygame.quit()
sys.exit()