import pyttsx3
import speech_recognition as sr
import cv2 as cv
import numpy as np
import mediapipe as mp 
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

global engine
engine = pyttsx3.init()
engine.setProperty('volume', 0.6)

def voice_in():
     try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            vo_in = r.recognize_google(audio)
        return commands(vo_in) 
     except:
         voice_out("Voice not recognized try again")
         voice_in()
def commands(vo_in):
        match vo_in:
            case "center":
                return "center"
            case "bottom left":
                return "bl"
            case "bottom right":
                return "br"
            case "top left":
                return "tl"
            case "top right":
                return "tr"
            case _:
                print("Nuh uh")
                voice_out("Command not recognized")
                return voice_in()
def voice_out(vo_out): 
    engine.say(vo_out)
    engine.runAndWait()

def take_image():

    webcam = cv.VideoCapture(0)
    success, image = webcam.read()
    image = cv.flip(image,1)# flips image horizontally
    return image

def processImg(image):
    #face detection using MediaPipe
    image = cv.cvtColor(image,cv.COLOR_BGR2RGB)
    results = mp_face_detection.process(image)

    #draw face detection annotations on the image
    image = cv.cvtColor(image,cv.COLOR_RGB2BGR)

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)

        bbox = detection.location_data.relative_bounding_box
        bbox_list = [bbox.xmin, bbox.ymin, bbox.width, bbox.height]
        xvalue = (bbox_list[0] + bbox_list[2])/2
        yvalue = (bbox_list[1] + bbox_list[3])/2
        return (xvalue,yvalue)
    else:
        return (None,None)

def convertFace(x,y):
    #take the coord and make it an accepted postion
    if(x == None and y == None):
        pos = "np"
    elif(((x < .24) and (y > .320))):
        pos = "bl" #center of object is in bottom left, as x and y positons are less than edges
    elif(((x < .240 ) and (y < .320))):
        pos = "tl" #center of object is in top left as x value is less than horizontal bound and y is greater than vertical bound
    elif (((x > .400) and (y > .320))):
        pos = "br" #in bottom right
    elif(((x > .400) and (y < .320))):
        pos = "tr" #in top right
    elif((x > .240) and (x < .400)):
        pos = "center" #temporary default
    else:
        pos = "np"
    #currently no case for the center being on a line or object is in multiple sections
    return pos

def reposition (gPos,curPos):

    while(gPos != curPos):
        if(gPos == 'tr'):
            match curPos:
                case "br":
                    voice_out("Move face Up")
                    time.sleep(3) #makes program waith 3 seconds
                case "tl":
                    voice_out("Move face right")
                    time.sleep(3)
                case "bl":
                    voice_out("Move face up and right")
                    time.sleep(3)
                case "center":
                    voice_out("Move face right")
                    time.sleep(3)
                case "np":
                    voice_out("Move face down and left")
                    time.sleep(3)
        elif(gPos == 'tl'):
            match curPos:
                case 'bl':
                    voice_out("Move face up")
                    time.sleep(3)
                case 'tr':
                    voice_out("Move face left")
                    time.sleep(3)
                case 'br':
                    voice_out("Move face up and left")
                    time.sleep(3)
                case "center":
                    voice_out("Move face left")
                    time.sleep(3)
                case "np":
                    voice_out("Move face down and right")
                    time.sleep(3)
        elif(gPos == 'br'):
            match curPos:
                case 'tr':
                    voice_out("Move face down")
                    time.sleep(3)
                case 'bl':
                    voice_out("Move face right")
                    time.sleep(3)
                case 'tl':
                    voice_out("Move face down and right")
                    time.sleep(3)
                case 'center':
                    voice_out("Move face right")
                    time.sleep(3)
                case 'np':
                    voice_out("Move face up and left")
                    time.sleep(3)
        elif (gPos == "bl"):
            match curPos:
                case 'tl':
                    voice_out("Move face down")
                    time.sleep(3)
                case 'br':
                    voice_out("Move face left")
                    time.sleep(3)
                case 'tr':
                    voice_out("Move face down and left")
                    time.sleep(3)
                case 'center':
                    voice_out("Move face left")
                    time.sleep(3)
                case 'np':
                    voice_out("Move face up and right")
                    time.sleep(3)
        elif gPos == 'center':
            match curPos:
                case 'bl':
                    voice_out("Move face right")
                    time.sleep(3)
                case 'tl':
                    voice_out("Move face right")
                    time.sleep(3)
                case 'tr':
                    voice_out("Move face left")
                    time.sleep(3)
                case 'br':
                    voice_out("Move face left")
                    time.sleep(3)
        
        image = take_image()
        coords = processImg(image) 
        curPos = convertFace(coords[0],coords[1])
        print("Your current position is: ", curPos, "goal: ", gPos)


    cv.imshow("Final",image)
    cv.imwrite("Final.jpg",image)


mp_face_detection = mp.solutions.face_detection.FaceDetection()
mp_drawing=mp.solutions.drawing_utils

voice_out("Welcome to the program get ready for your selfie")

image = take_image()
coords = processImg(image)
position = convertFace(coords[0],coords[1])

voice_out("Your face is currently in position, " + position +
          ". What position would you like your face to be in?")
goalPos = "RAHHHHHH"
goalPos = voice_in()
print(goalPos)
if position == goalPos:
    cv.imshow("Final",image)
    time.wait(5)
    cv.imwrite("Final.jpg",image)
else:
    reposition(goalPos,position)
