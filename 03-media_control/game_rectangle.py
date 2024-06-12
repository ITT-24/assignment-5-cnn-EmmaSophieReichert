# this is a copy from the file from assignment 4: https://github.com/ITT-24/assignment-4-markers-and-computer-vision-EmmaSophieReichert/blob/master/ar_game/game_rectangle.py
#this file was inspired by arucy_sample.py and finished task 1

import cv2
import cv2.aruco as aruco
import numpy as np

# Define the ArUco dictionary and parameters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
aruco_params = aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

left_upper = None
right_upper = None
right_down = None
left_down = None

# used GPT for this method - stores selected points in the right order
def order_points(corners, ids) -> list:
    global left_upper, right_upper, right_down, left_down
    for i in range(0, len(ids)):
        if(ids[i][0] == 0):
            left_upper = corners[i][0][2] #get inner corners
        elif(ids[i][0] == 1):
            right_upper = corners[i][0][3]
        elif(ids[i][0] == 2):
            right_down = corners[i][0][0]
        elif(ids[i][0] == 3):
            left_down = corners[i][0][1] 
    return [left_upper, right_upper, left_down, right_down]  

def get_wrapped_result(corners, frame) -> list:
    height, width, _ = frame.shape #looked this up in Luca Eschers solution
    pts1 = np.float32(corners)
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    
    M = cv2.getPerspectiveTransform(pts1, pts2)
    
    return cv2.warpPerspective(frame,M,(width, height))

current_corners = []

def get_game_rectangle(cap) -> tuple[list, bool]:
    global current_corners
    ret, frame = cap.read()
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers in the frame
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

    # Check if marker is detected
    if ids is not None:
        # Draw lines along the sides of the marker
        aruco.drawDetectedMarkers(frame, corners)

        if len(corners) == 4 and len(ids) == 4: #all four markers detected
            current_corners = order_points(corners, ids) #store the positions of the markers against flickering and order them
        if len(current_corners) == 4: # all four markers are stored before
            return get_wrapped_result(current_corners, frame), True
        
    return frame, False