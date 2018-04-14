
## Real time video from webcamera

import numpy as np
import cv2

fps = 30

def getImage():
    cv2.namedWindow("webcam-feed")
    cam = cv2.VideoCapture(0)

    if cam.isOpened(): # try to get the first frame
        ret, frame = cam.read()
    else:
        ret = False
    frames = 1;
    img_counter = 0
    while ret:
        cv2.imshow("webcam-feed", frame)
        ret, frame = cam.read()
        frames+=1
        ## ==============
        ## what is waitkey
        ## ===============
        key = cv2.waitKey(20) # milliseconds
        if frames%30 == 0:
            print("Time: {} secs \r".format(int(frames/fps)),end="")
        if key==27 : # ESC pressed
            print("\nEscape hit, closing...")
            break

        if key == 32:  # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    cv2.destroyWindow("webcam-feed")

getImage()
