import cv2
import numpy as np
from arg_parser import get_parsed_arguments
import sys

def mouse_callback(event, x, y, flags, param):
    global img, orig_img, points, output, width, height

    if event == cv2.EVENT_LBUTTONDOWN:
        img = cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        points.append([x, y])
        if len(points) == 8:
            pts1 = np.float32(points[4:])
            pts2 = np.float32(points[:4])
            M = cv2.getPerspectiveTransform(pts1,pts2)
            # change height and width ??
            img = cv2.warpPerspective(img,M,(height - 1, width - 1))
        cv2.imshow(WINDOW_NAME, img)
            
        key = cv2.waitKey(0)
        if key == 27:  # restart on esc
            points = points[:4]
            img = orig_img.copy()
            cv2.imshow(WINDOW_NAME, img)
        elif key == ord('s'):
            cv2.imwrite("new_sample_img.png", img)

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
    input, output, width, height = get_data_depending_on_input()

    img = cv2.imread(input)
    orig_img = img.copy()
    WINDOW_NAME = 'Preview Window'

    #height, width, _ = img.shape
    points = [[0,0],[height - 1,0],[0,width - 1],[height - 1,width - 1]]

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
    cv2.imshow(WINDOW_NAME, img)
    cv2.waitKey(0)
