
## Real time video from webcamera


import numpy as np
import cv2

# parameters

threshold = 100  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 100

# Constants for finding range of skin color in YCrCb
min_YCrCb = np.array([0,133,77],np.uint8)
max_YCrCb = np.array([255,173,127],np.uint8)

fps = 30

def getImage():
    cv2.namedWindow("webcam-feed")
    cam = cv2.VideoCapture(0)

    if cam.isOpened(): # try to get the first frame
        ret, frame = cam.read()
    else:
        ret = False
    frames = 1
    timer = 0
    img_counter = 0
    while ret:

        ret, frame = cam.read()
        #color = np.uint8([[[blue, green, red]]])
        #hsv_color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #defining the Range of yellow color
        yellow_lower=np.array([22,60,120],np.uint8)
        yellow_upper=np.array([60,255,255],np.uint8)

        #finding the range of yellow color in the image
        yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)

        #Morphological transformation, Dilation
        kernal = np.ones((5 ,5), "uint8")

        yellow=cv2.dilate(yellow,kernal)
        res2=cv2.bitwise_and(frame, frame, mask = yellow)

        '''
        #Tracking the Red Color
        (_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>300):
                x,y,w,h = cv2.boundingRect(contour)
                img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
        '''



        mask = np.zeros(frame.shape[:-1],np.uint8)
        height, width = frame.shape[:-1]
        mask1 = np.zeros((height+2, width+2), np.uint8)     # line 26
        cv2.floodFill(mask,mask1,(0,0),255)     # line 27

        #Tracking the yellow Color
        (_,contours,hierarchy)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        areaMax = 100
        x = 0
        y = 0
        w = 0
        h = 0
        area = 00
        bigContour = None
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > areaMax:
                areaMax = area
                bigContour = contour

        x,y,w,h = cv2.boundingRect(bigContour)
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        res2 = cv2.rectangle(res2,(x,y),(x+w,y+h),(0,255,0),2)
        # Write some Text
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,500)
        position = (int(x+h/2),int(y+h/2))
        fontScale = 1
        fontColor = (0,255,0)
        lineType  = 2
        cv2.imshow("Color Tracking",frame)
        cv2.putText(res2,"+", position,font,fontScale,fontColor,lineType)

        #cv2.putText(res2,"yellow",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))

        #cv2.imshow("Redcolour",red)
        #cv2.imshow("red",res)
        cv2.imshow("yellow",res2)

        frames+=1
        timer = int(frames/fps)
        key = cv2.waitKey(20) # milliseconds
        if frames%30 == 0:
            print("Time: {} secs \r".format(timer),end="")
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
    cv2.destroyWindow("yellow")

getImage()
