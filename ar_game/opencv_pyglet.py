import cv2
import numpy as np
import pyglet
from PIL import Image
import sys
import cv2.aruco as aruco
from Bubbles import Bubbles
from Game import BubbleGame
import config as c
from typing import List, Any
from imutils import perspective

video_id = 0
if len(sys.argv) > 1:
  video_id = int(sys.argv[1])

# Define the ArUco dictionary and parameters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
aruco_params = aruco.DetectorParameters()

# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)
resolution = cap.read()[1].shape
c.Window.HEIGHT = resolution[0]
c.Window.WIDTH = resolution[1]
window = pyglet.window.Window(c.Window.WIDTH, c.Window.HEIGHT)

game = BubbleGame()

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

def detect_markers(frame:List[Any]) -> List[Any]:
    """detect the four markers"""
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers in the frame
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    # Check if marker is detected
    if ids is not None:
        # Draw lines along the sides of the marker
        aruco.drawDetectedMarkers(frame, corners)
    return frame, corners

# order_points_new from https://gist.github.com/flashlib/e8261539915426866ae910d55a3f9959
def order_points_new(pts):
    """ordering coordinates clockwise"""
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
    (tr, br) = rightMost

    return np.array([tl, tr, br, bl], dtype="float32")

def warp_image(frame:List[Any], markers:List[Any]) -> List[Any]:
    """warp image -> the four markers are the new corners"""
    height, width, _ = frame.shape
    corners = np.float32([[0,0],[width - 1,0],[0,height - 1],[width - 1,height - 1]])
    corner_markers = []
    idx = 0
    for marker in markers:
      marker[0] = order_points_new(marker[0])
      corner_markers.append(marker[0][idx])
      idx += 1
    corner_markers = np.float32(corner_markers)
    M = cv2.getPerspectiveTransform(corner_markers,corners)
    frame = cv2.warpPerspective(frame,M,(width - 1, height - 1))
    return frame

def detect_finger(frame:List[Any]) -> List[Any]:
    """detect a finger or other object in the frame with edge detection"""
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #img_contours = cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)
    img_contours = np.flip(img_contours, axis=0)
    return img_contours, contours
    

@window.event
def on_draw():
    window.clear()
    ret, frame = cap.read()
    frame, markers = detect_markers(frame)
    if len(markers) == 4:
      frame = warp_image(frame, markers)
      frame, contours = detect_finger(frame)
      game.score = Bubbles.handle_collision_with(contours, game.score)
      
    img = cv2glet(frame, 'BGR')
    img.blit(0, 0, 0)
    game.draw_game()
    game.update_game()


pyglet.app.run()
