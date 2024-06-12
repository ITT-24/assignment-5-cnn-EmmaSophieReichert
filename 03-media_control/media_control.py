from keras.models import load_model
import pygame
import time
import sys
import cv2
from mapping_and_config import LABELS, IMG_SIZE, SIZE
import game_rectangle
import numpy as np
from matplotlib import pyplot as plt

INPUT_PATH = "adventure.mp3"
cam_index = 0
COLOR_CHANNELS = 3

if len(sys.argv) > 1:
    INPUT_PATH = str(sys.argv[1])
    if len(sys.argv) > 2:
        cam_index = int(sys.argv[2])

print("CAMERA ", cam_index)
cap = cv2.VideoCapture(cam_index)

model = load_model("gesture_recognition.keras")

# this class was originally generated with GPT and then modified
class MediaController:
    def __init__(self, media_file):
        pygame.mixer.init()
        self.media_file = media_file
        self.volume = 0.5
    def play(self):
        pygame.mixer.music.load(self.media_file)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        print(f'Playing: {self.media_file}')

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print('Paused')

    def unpause(self):
        pygame.mixer.music.unpause()
        print('Unpaused')

    def stop(self):
        pygame.mixer.music.stop()
        print('Stopped')

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)
        print(f'Volume set to: {volume}')

    def increase_volume(self):
        self.volume = self.volume + 0.05
        if(self.volume > 1):
            self.volume = 1
        pygame.mixer.music.set_volume(self.volume)
        print(f'Volume set to: {self. volume}')
    
    def decrease_volume(self):
        self.volume = self.volume - 0.05
        if(self.volume < 0):
            self.volume = 0
        pygame.mixer.music.set_volume(self.volume)
        print(f'Volume set to: {self. volume}')

    def is_playing(self):
        return pygame.mixer.music.get_busy()

controller = MediaController(INPUT_PATH)
controller.play()

def get_image():
    frame, detection = game_rectangle.get_game_rectangle(cap) #get the current camera frame; get a snipped version, if markers were once detected
    resized = cv2.resize(frame, SIZE)
    #cv2.imshow('Resized Image', frame)
    #cv2.waitKey(0)
    return resized.reshape(-1, IMG_SIZE, IMG_SIZE, COLOR_CHANNELS)

while True:
    image = get_image()
    
    prediction = model.predict(image)
    gesture = LABELS[np.argmax(prediction)]
    print(gesture)
    if(gesture == "like"):
        controller.increase_volume()
    if(gesture == "dislike"):
        controller.decrease_volume()
    if(gesture == "stop"):
        controller.pause()
    time.sleep(2)