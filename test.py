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

def voice_in(object =0):
     try:
        r = sr.Recognizer()
        with sr.Microphone(sample_rate=16000) as source:
            audio = r.listen(source, timeout=10, phrase_time_limit=3)
            vo_in = r.recognize_google(audio, language='en-US')
        if object:
            return vo_in
        return commands(vo_in)
     except sr.WaitTimeoutError:
        print("bruh")
        return 1
def commands(vo_in):
    if "help" in vo_in:
        #Find last word, hopefully the command
        words = list(vo_in.split(" "))
        length = len(words)
        vo_in = words[len-1]
        match vo_in:
            case _: 
                print("Nuh uh")
    else:
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
                voice_in()

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
        
        voice_out("Get ready for new selfie")
        image = take_image()
        voice_out("New image taken")
        coords = processImg(image) 
        curPos = convertFace(coords[0],coords[1])
        print("Your current position is: ", curPos, "goal: ", gPos)


    cv.imshow("FinalFace",image)
    cv.imwrite("FinalFace.jpg",image)


mp_face_detection = mp.solutions.face_detection.FaceDetection()
mp_drawing=mp.solutions.drawing_utils

voice_out("Welcome to the program get ready for your selfie")

image = take_image()
voice_out("Selfie taken")
coords = processImg(image)
position = convertFace(coords[0],coords[1])

voice_out("Your face is currently in position, " + position +
          ". What position would you like your face to be in?")
goalPos = voice_in()
print(goalPos)
if position == goalPos:
    cv.imshow("FinalFace",image)
    cv.imwrite("FinalFace.jpg",image)
else:
    reposition(goalPos,position)
