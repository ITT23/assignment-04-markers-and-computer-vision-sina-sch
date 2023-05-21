import cv2
import numpy as np
import pyglet
from PIL import Image
import sys
import cv2.aruco as aruco
from Bubbles import Bubbles


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360

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

def detect_markers(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers in the frame
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    # Check if marker is detected
    if ids is not None:
        # Draw lines along the sides of the marker
        aruco.drawDetectedMarkers(frame, corners)
    return frame, corners

def warp_image(frame, markers):
    height, width, _ = frame.shape
    corners = np.float32([[0,0],[width - 1,0],[0,height - 1],[width - 1,height - 1]])
    corner_markers = []
    i = [2, 1, 0, 3]
    idx = 0
    for marker in markers:
       corner_markers.append(marker[0][i[idx]])
       idx += 1
    corner_markers = np.float32(corner_markers)
    M = cv2.getPerspectiveTransform(corner_markers,corners)
    frame = cv2.warpPerspective(frame,M,(width - 1, height - 1))
    #img = cv2.resize(img, (result_width, result_height), interpolation = cv2.INTER_AREA)
    return frame

def detect_finger(frame):
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
      Bubbles.handle_collision_with(contours)
      
    img = cv2glet(frame, 'BGR')
    img.blit(0, 0, 0)
    Bubbles.draw_bubbles()
    Bubbles.update_bubbles()



if __name__ == "__main__":
  video_id = 0
  if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

  # Define the ArUco dictionary and parameters
  aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
  aruco_params = aruco.DetectorParameters()

  # Create a video capture object for the webcam
  cap = cv2.VideoCapture(video_id)
  bubbles = Bubbles.create_bubbles()

  pyglet.app.run()
