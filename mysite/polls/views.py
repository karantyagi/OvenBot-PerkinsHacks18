from django.template.response import TemplateResponse

## Real time video from webcamera
import numpy as np
import cv2

# from urllib import parse, error
import base64
import requests
import json
import cv2
import io
from google.cloud.vision import types

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/quazar07/Desktop/perkins_hackathon/perkins-hackathon-OCR-b116d4935f42.json"

from google.cloud import vision

def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

def index(request):
    if request.method == "GET":
            return TemplateResponse(request, 'index.html', {})
    else:
        data= my_response(request.POST.get('text_val'))
        return TemplateResponse(request, 'index.html',data)

def getImage():
    cv2.namedWindow("webcam-feed")
    cam = cv2.VideoCapture(0)

    if cam.isOpened(): # try to get the first frame
        ret, frame = cam.read()
    else:
        ret = False

    img_counter = 0
    while ret:
        cv2.imshow("webcam-feed", frame)
        ret, frame = cam.read()
        ## ==============
        ## what is waitkey
        ## ===============
        key = cv2.waitKey(20)
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

def my_response(seq):
    # Call webcam function
    getImage()

    # Get text
    path = '/home/quazar07/Desktop/perkins_hackathon/cut_image.png'
    detect_text()

    # Call IBM WATSON API
    import win32com.client as wincl
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(seq)    # Speak out instruction
    # Prints a success on the screen
    resp = {'key':'success'}
    return resp
