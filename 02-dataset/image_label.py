# modified code from Stefan Röhr: https://github.com/ITT-24/assignment-5-cnn-Sro12343/tree/master/ImageLabel

import cv2
import numpy as np
import pyglet
from pyglet.window import mouse
from PIL import Image
import sys
import os
import json

#setup variables    
current_dir = os.path.dirname(__file__)
input_path = os.path.join(current_dir,'sample_image.jpg')
resolution_x = 1920 #100
resolution_y = 1080 #100
point_list_x = []
point_list_y = []
poseType = ""

#check Command line parameters
if len(sys.argv) > 2:
    input_path = sys.argv[1]
    #output_path = sys.argv[2]
    poseType = sys.argv[2]
else:
    print("Not enough entries: Using ./sample_image.jpg ./result_image.jpg x=100 y=100")

#Load image
source_img = cv2.imread(input_path)

print(f"Trying to load image from: {input_path}")
edit_img = source_img.copy()  
print("shape")
print(source_img.shape)
height, width = source_img.shape[:2]

new_dimensions = (width // 2, height // 2)
edit_img = cv2.resize(source_img, new_dimensions, interpolation=cv2.INTER_AREA)
width =int(width/2)
height = int(height/2)
#Setup Pyglet Window
WINDOW_WIDTH = width
WINDOW_HEIGHT = height
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)


# converts OpenCV image to PIL image and then to pyglet texture
# https://gist.github.com/nkymut/1cb40ea6ae4de0cf9ded7332f1ca0d55
def cv2glet(img,fmt):
    '''Assumes image is in BGR color space. Returns a pyimg object'''
    if fmt == 'GRAY':
      rows, cols = img.shape
      channels = 1
    else:
      rows, cols, channels = img.shape

    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols, 
                                   height=rows, 
                                   fmt=fmt, 
                                   data=raw_img, 
                                   pitch=top_to_bottom_flag*bytes_per_row)
    return pyimg

@window.event
def on_draw():
    #global edit_img
    window.clear()
    show_img = cv2glet(edit_img, 'BGR')
    show_img.blit(0, 0, 0)
    
#React to mouse clicks
@window.event
def on_mouse_press(x, y, button, modifiers):
    global edit_img
    global point_list_x
    global point_list_x
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global poseType
    global input_path
    global source_img
    if button == mouse.LEFT:
        if len(point_list_x) < 2:
            #Not enough points jet
            point_list_x.append(x)
            point_list_y.append(WINDOW_HEIGHT-y)
            edit_img = cv2.circle(edit_img, (x, height-y), 5, (255, 0, 0), -1)
        if len(point_list_x) == 2:
            inner_content = '''"bboxes": 
            [
                [
                    {},
                    {},
                    {},
                    {}
                ]
            ],
            "labels": 
            [
                "{}"
            ]'''.format(point_list_x[0] / WINDOW_WIDTH,
                        point_list_y[0] / WINDOW_HEIGHT,
                        (point_list_x[1] - point_list_x[0]) / WINDOW_WIDTH,
                        (point_list_y[1] - point_list_y[0]) / WINDOW_HEIGHT,
                        poseType)

            print('"{}":\n{{\n{}\n}}'.format(os.path.basename(input_path)[:-4], inner_content)) #changed this to just pic the image name
            height2, width2 = source_img.shape[:2]
            
            #Enough points so warp image
            point_array = np.float32(np.array([[0, 0], [width2, 0], [width2, height2], [0, height2]]))
            #point_array = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
            print(height2, width2)
            if(height2 > width2): #portrait format
                destination = np.float32(np.array([[0, 0], [resolution_y, 0], [resolution_y, resolution_x], [0, resolution_x]]))
                mat = cv2.getPerspectiveTransform(point_array, destination)
                edit_img = cv2.warpPerspective(source_img,mat,(resolution_y, resolution_x)) #use final resulution here!!
            else: #landscape format
                destination = np.float32(np.array([[0, 0], [resolution_x, 0], [resolution_x, resolution_y], [0, resolution_y]]))
                mat = cv2.getPerspectiveTransform(point_array, destination)
                edit_img = cv2.warpPerspective(source_img,mat,(resolution_x, resolution_y)) #use final resulution here!!
            print("SHAPE: ", edit_img.shape)
            cv2.imwrite(input_path, edit_img)
            #resize to result resolution
            window.close()        

pyglet.app.run()