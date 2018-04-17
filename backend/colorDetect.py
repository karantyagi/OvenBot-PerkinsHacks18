
## Real time video from webcamera

from __future__ import division
from google.cloud import vision
import numpy as np
import cv2
import win32com.client as wincl
import time
import base64
import requests
import json
import cv2
import io
from google.cloud.vision import types
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances as ED
import math
import sys
import os
from difflib import SequenceMatcher
import winsound


input = sys.argv[1]
freq = 5

# path to google APi json file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="googleAPI/perkins-hackathon-OCR-b116d4935f42.json"


def detect_text(path):
    centroids_list = []
    text_list = []
    cordinates_list = []

    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        # print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        temp_list = []
        for vertex in text.bounding_poly.vertices:
            temp_list.append((vertex.x,vertex.y))
        cordinates_list.append(temp_list)
        vertices_temp = [(each.x,each.y) for each in text.bounding_poly.vertices]
        c_x= 0
        c_y= 0
        for each in vertices_temp:
            c_x+= each[0]
            c_y+= each[1]
        c_x/=4
        c_y/=4
        centroids_list.append((c_x,c_y))
        text_list.append(text.description)

        # print('bounds: {}'.format(','.join(vertices)))
    return centroids_list,text_list,cordinates_list


def get_euclidean_distance(x,y):
    return(math.pow(x[0]-y[0],2)+math.pow(x[1]-y[1],2))


def get_merging_indices(c):
    l = len(c)
    min_dist =0
    if(l>2):
        min_dist = get_euclidean_distance(c[1],c[2])
        for i in range(1,l):
            for j in range(1,l):
                if(i!=j):
                    if(get_euclidean_distance(c[i],c[j]) < min_dist):
                        min_dist = get_euclidean_distance(c[i],c[j])
    merging_indices = []
    for i in range(1,l):
            for j in range(1,l):
                if(i!=j):
                    if(get_euclidean_distance(c[i],c[j]) < (1.20)*min_dist):
                        if((i,j) not in merging_indices and (j,i) not in merging_indices):
                            merging_indices.append((i,j))
    return merging_indices

def merge_(indices,coords,t):
    temp_coords = []
    temp_t = []
    for each in indices:
        x1 = [vertex[0] for
              vertex in coords[each[0]]]
#         print(coords[each[1]])
        x2 = [vertex[0] for vertex in coords[each[1]]]
        y1 = [vertex[1] for vertex in coords[each[0]]]
        y2 = [vertex[1] for vertex in coords[each[1]]]
        x_min =min([min(x1),min(x2)])
        x_max = max([max(x1),max(x2)])
        y_min = min([min(y1),min(y2)])
        y_max = max([max(y1),max(y2)])
        temp_coords.append([(x_min,y_min),(x_max,y_min),(x_max,y_max),(x_min,y_max)])
        temp_t.append(t[each[0]]+" "+t[each[1]])
#         coords.pop(each[0])
#         coords.pop(each[1])
    return temp_coords,temp_t


def get_merged_lists(merging_indices,coords,t):
    delete_indices = []
    for each in merging_indices:
        delete_indices.append(each[0])
        delete_indices.append(each[1])
    new_t = []
    new_coords = []
    for i in range(len(coords)):
        if(i not in delete_indices):
            new_coords.append(coords[i])
            new_t.append(t[i])
    return new_t,new_coords


def get_centroid(coords,ind):
    avg_x=0
    avg_y=0
    for each in coords[ind]:
        avg_x+=each[0]
        avg_y+=each[1]
    return((avg_x/4,avg_y/4))

def beep_gps(curr,goal_ind,coords):
    max_dist = get_euclidean_distance(coords[0][0],coords[0][2])/2
    freq = 1
    if(is_inside(curr,goal_ind,coords)==1):
        freq = 0
        return
    else:
        cent = get_centroid(coords,goal_ind)
        dist = get_euclidean_distance(curr,cent)
        ratio = dist/max_dist
        if(ratio<0.2):
            freq = 5
        elif(ratio<0.3):
            freq = 4
        elif(ratio<0.5):
            freq= 3
        elif(ratio<0.7):
            freq = 2
        else:
            freq = 1
    return freq

def is_inside(curr,goal_ind,new_coords):
    x = curr[0]
    y = curr[1]
    ax = new_coords[goal_ind][0][0]
    ay = new_coords[goal_ind][0][1]

    bx = new_coords[goal_ind][1][0]
    by = new_coords[goal_ind][1][1]

    dx = new_coords[goal_ind][2][0]
    dy = new_coords[goal_ind][2][1]

    bax = bx - ax
    bay = by - ay
    dax = dx - ax
    day = dy - ay

    if ((x - ax) * bax + (y - ay) * bay < 0.0):
        return 0
    if ((x - bx) * bax + (y - by) * bay > 0.0):
        return 0
    if ((x - ax) * dax + (y - ay) * day < 0.0):
        return 0
    if ((x - dx) * dax + (y - dy) * day > 0.0):
        return 0

    return 1

def gps(curr,goal_ind,coords):
    if(is_inside(curr,goal_ind,coords)==1):
        print('Reached!')
        return('Reached')
    else:
        cent = get_centroid(coords,goal_ind)
        ans = ""
        if(curr[1]>=coords[goal_ind][0][1] and curr[1]<=coords[goal_ind][2][1] ):
            ans+=""
        elif(cent[1]>curr[1]):
            ans+="down"
        elif(cent[1]<curr[1]):
            ans+="up"
        if(curr[0]>=coords[goal_ind][0][0] and curr[0]<=coords[goal_ind][1][0] ):
            ans+=""
        elif(cent[0]>curr[0]):
            ans+=" left"
        elif(cent[0]<curr[0]):
            ans+=" right"
        print(ans)
        return(ans)

def longestcommonsubstring(string1,string2):
    match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    return(string1[match.a: match.a + match.size])

#########

## time.sleep(5)   # delays for 5 seconds. You can Also Use Float Value.

# parameters
# Constants for finding range of skin color in YCrCb
timer = 0
fps = 30

def startLoop():
    global freq
    #cv2.namedWindow("webcam-feed")
    cam = cv2.VideoCapture(0)
    base = cv2.imread(path1)
    if cam.isOpened(): # try to get the first frame
        ret, frame = cam.read()
    else:
        ret = False
    frames = 1
    timer = 0
    img_counter = 0
    while ret:

        ret, frame = cam.read()
        frame = cv2.flip(frame,1)
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
        areaMax = 200
        x = 0
        y = 0
        w = 0
        h = 0
        area = 0
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
        position = (int(x+(w/2)),int(y+(h/2)))
        fontScale = 1
        fontColor = (0,255,0)
        lineType  = 1
        cv2.putText(base,"+", position,font,fontScale,fontColor,lineType)
        cv2.imshow("Color Tracking",base)
        cv2.putText(res2,"+", position,font,fontScale,fontColor,lineType)

        #cv2.putText(res2,"yellow",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))

        #cv2.imshow("Redcolour",red)
        #cv2.imshow("red",res)
        cv2.imshow("yellow",frame)

        frames+=1
        timer = frames/fps
        if frames % 6 == 0:
            curr = (x,y)
            #beep_gps(curr,goal_index,coords)
# ##################################################################
            goal_index = 2
# HARD CODED GOAL INDEX TO 1
#####################################################################

            freq = beep_gps(curr,goal_index,new_coords1)
            speak_out = gps(curr,goal_index,new_coords1)
            print("X {} Y: {}".format(x,y))
            #speak = wincl.Dispatch("SAPI.SpVoice")
            #speak.Speak(speak_out)
            #print("\a")
            frequency = 500  # Set Frequency To 2500 Hertz
            duration = 6  # Set Duration To 1000 ms == 1 second

            if freq == 1 and frames % 30 == 0:
                frequency = 100
                winsound.Beep(frequency, duration)
            elif freq == 2 and frames % 24 == 0:
                frequency = 400
                winsound.Beep(frequency, duration)
            elif freq == 3 and frames % 18 == 0:
                frequency = 1000
                winsound.Beep(frequency, duration)
            elif freq == 4 and frames % 12 == 0:
                frequency = 1800
                winsound.Beep(frequency, duration)
            elif freq == 5 and frames % 6 == 0:
                frequency = 2500
                winsound.Beep(frequency, duration)

            print("Msg: {} at time : {} sec".format(speak_out,timer))
            frame+=1
            timer = frames/fps
            if speak_out=='Reached':
                speak = wincl.Dispatch("SAPI.SpVoice")
                speak.Speak(speak_out)

                break



        key = cv2.waitKey(20) # milliseconds
        if frames%30 == 0:
            print("Time: {} secs \r".format(timer),end="")
        if key==27 : # ESC pressed
            print("\nEscape hit, closing...")
            break

        if key == 32:  # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #gray_image = cv2.flip(gray_image,1)
            cv2.imwrite(img_name, cv2.flip(frame,1))
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()
    cv2.destroyWindow("yellow")

def longestcommonsubstring(string1,string2):
    match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    return(string1[match.a: match.a + match.size])

def get_index_from_text(text,t):
    max_len = 0
    max_ind = -1
    for i in range(1,len(t)):
#         print(longestSubstringFinder(text,t[i]))
        t_len = len(longestcommonsubstring(text,t[i]))
#         print(t_len)
#         print(t[i])
        if(t_len>max_len):
            max_len = t_len
            max_ind = i
    return(max_ind)



############## START RUN ###########

# base map
#
path1 = 'testImages/basemap.png'

c1,t1,coords1 = detect_text(path1)
merging_indices1 = get_merging_indices(c1)
# coords = list(original_coords)
# t = list(original_t)
temp_coords,temp_t = merge_(merging_indices1,coords1,t1)
coords1.extend(temp_coords)
t1.extend(temp_t)

new_t1 = []
new_coords1 = []
new_t1,new_coords1  = get_merged_lists(merging_indices1,coords1,t1)

for i in range(1,len(new_t1)):
    print(new_t1[i])
    print(i)
    print()

if input.lower() == "start":
    startLoop() ### start infinite loop


'''
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
  '''
