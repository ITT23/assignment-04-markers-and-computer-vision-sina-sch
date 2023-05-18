import cv2
import numpy as np
from matplotlib import pyplot as plt
import copy

img = cv2.imread('image_extraction/sample_image.jpg')
# idea with cache from https://stackoverflow.com/questions/33548150/how-to-delete-drawn-lines-on-image-in-python
cache = copy.deepcopy(img)
WINDOW_NAME = 'Preview Window'

rows, cols ,_ = img.shape
points = [[0,0],[rows - 1,0],[0,cols - 1],[rows - 1,cols - 1]]

cv2.namedWindow(WINDOW_NAME)

def mouse_callback(event, x, y, flags, param):
    global img
    global cache
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        img = cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        points.append([x, y])
        print(points)
        if len(points) == 8:
            pts1 = np.float32(points[4:])
            pts2 = np.float32(points[:4])
            M = cv2.getPerspectiveTransform(pts1,pts2)
            img = cv2.warpPerspective(img,M,(rows - 1,cols - 1))
            cv2.imshow(WINDOW_NAME, img)
            key = cv2.waitKey(0)
            if key == 27:  # restart on esc
                points = points[:4]
                img = cache
                cv2.imshow(WINDOW_NAME, img)

        else:
            cv2.imshow(WINDOW_NAME, img)


cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

cv2.imshow(WINDOW_NAME, img)

cv2.waitKey(0)
