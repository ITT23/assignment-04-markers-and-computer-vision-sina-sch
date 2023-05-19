import cv2
import numpy as np
from arg_parser import get_parsed_arguments
import sys

def mouse_callback(event, x, y, flags, param):
    global img, orig_img, points, output, result_width, result_height

    if event == cv2.EVENT_LBUTTONDOWN:
        img = cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        points.append([x, y])
        if len(points) == 8:
            pts = bring_in_right_order(points)
            pts = np.float32(pts)
            corners = np.float32(points[:4])
            M = cv2.getPerspectiveTransform(pts,corners)
            # change height and width ??
            img = cv2.warpPerspective(img,M,(width - 1, height - 1))
            img = cv2.resize(img, (result_width, result_height), interpolation = cv2.INTER_AREA)
        cv2.imshow(WINDOW_NAME, img)
            
        key = cv2.waitKey(0)
        if key == 27:  # restart on esc
            points = points[:4]
            img = orig_img.copy()
            cv2.imshow(WINDOW_NAME, img)
        elif key == ord('s'):
            cv2.imwrite("new_sample_img.png", img)

def bring_in_right_order(points):
    pts = points[4:]
    corners = points[:4]
    vectors = []
    new_pts = pts.copy()
    for pt in pts:
        for corner in corners:
            vectors.append(measure_distance(pt[0], pt[1], corner[0], corner[1]))
        nearest_corner = corners[vectors.index(np.min(vectors))]
        idx = corners.index(nearest_corner)
        new_pts[idx] = pt
        vectors = []
    return new_pts
        

# function from pyglet_click.py
def measure_distance(x1, y1, x2, y2):
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance

def get_data_depending_on_input():
    args = get_parsed_arguments()
    print(args)
    if not args.input is None:
        input = args.input
    if not args.output is None:
        output = args.output
    if not args.width is None:
        width = args.width
    if not args.height is None:
        height = args.height

    try:
        return input, output, width, height
    except:
        print("Specify all required arguments.")
        sys.exit()


if __name__ == "__main__":
    input, output, result_width, result_height = get_data_depending_on_input()

    img = cv2.imread(input)
    orig_img = img.copy()
    WINDOW_NAME = 'Preview Window'

    height, width, _ = img.shape
    points = [[0,0],[width - 1,0],[0,height - 1],[width - 1,height - 1]]

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
    cv2.imshow(WINDOW_NAME, img)
    cv2.waitKey(0)
