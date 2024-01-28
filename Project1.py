#import for speech and text
import pyttsx3 
#imports for taking images and face + object detection
import cv2 as cv
import mediapipe as mp
import ultralytics
#import speech to text file
import speech_recognition as sr
#setting up object detection using the ultralytics library and yolov8 model and training set
import PIL
from ultralytics import YOLO
from PIL import Image
import time
import numpy as np
ultralytics.checks()
model = YOLO("yolov8n.pt") #loads the pretrained yolov8 model to save time when application is in use

#setting up mediapipe package for face detection
mp_face_detection= mp.solutions.face_detection.FaceDetection()
mp_drawing = mp.solutions.drawing_utils

#setting up opencv to use webcam
webcam = cv.VideoCapture(0)
    
#false = selfie true = subject
#Could we have the spacebar interupt the program at any time and allow for command input? Or just something to allow user input at any time?
cameramode = False

def main():
    #try:
        #engine.onError(voice_output, "VoiceError")
        global engine 
        engine = pyttsx3.init()
        engine.setProperty('volume', 0.6)
        voice_out("Hello welcome to the program. Would you like to take a selfie, or photograph an object?")
        voice_in()
    #except Exception as e:
        #Print details of the exception
        #print(f"An exception occurred: {type(e).__name__}")
        #print(f"Exception details: {e}")

def commands(vo_in):
    if "help" in vo_in:
        #Find last word, hopefully the command
        words = list(vo_in.split(" "))
        length = len(words)
        vo_in = words[len-1]
        match vo_in:
            case _: 
                print("Nuh uh")
    elif vo_in.isnumeric():
        return int(vo_in)/100
    else:
        match vo_in:
            case "commands":
                #list avalible commands
                voice_out("stored as list")
            case "home":
                #idk about this one
                main()
            case "selfie":
                image = take_photo(0)
                curpos = processFace(image)
                checkFace(curpos,image)
            case "object":
                image = take_photo(1)
                curpos = processObjs(image)
            case "change object": #repeat effect but I felt like we needed the option to change object.
                take_photo(1) 
                curpos = processObjs(image)
            case "position?":#I cant think of the correct word but like the framing of the object? Like centered and all that
                voice_out("#Variable storing current object position") 
            case "yes":
                return True
            case "no":
                return False
            case "center":
                return "c"
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


def voice_in(object=0):
    try:
        r = sr.Recognizer()
        with sr.Microphone(sample_rate=16000) as source:
            audio = r.listen(source, timeout=10, phrase_time_limit=3)
            vo_in = r.recognize_google(audio)
        if object:
            return vo_in
        return commands(vo_in)
    except sr.WaitTimeoutError:
        return 1

def voice_out(vo_out):
    engine.say(vo_out)
    engine.runAndWait()

def take_photo(cameramode):
    image = PIL.Image.open("Batman.png")
    if cameramode == 0:
        #Selfie option
        
        voice_out("Are you ready for the selfie?")
        if voice_in() == False:
            voice_out("Say yes when ready")
            voice_in()
            #Take a little silly photo
            succ, image = webcam.read()
            image = cv.flip(image,1) #flips the image horizontally
            image.show()
            return image
    else:
        #Object option
        voice_out("Are you ready for the static image?")
        if voice_in() == False:
            voice_out("Say yes when ready")
            voice_in()
            succ, image = webcam.read()
            image = cv.flip(image,1) #flips image horizontally
            image.show()
            return image

    return image

def processFace(image):
    image2 = cv.cvtColor(np.array(image),cv.COLOR_BGR2RGB) #changes color scale to allow mediapipe image processing
    results = mp_face_detection.process(image2) #uses face detection model to find faces in image
    image2 = cv.cvtColor(image2,cv.COLOR_RGB2BGR) #return image to original color scale

    #draw face detection annotations 
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image2,detection) #all changes+annotations made to seperate image so clean version can be saved

        #gets location of face
        bbox = detection.location_date.relative_bounding_box
        bbox_list = [bbox.xmin, bbox.ymin, bbox.width, bbox.height] #xmin and ymin are the coordiantes of the bottom left of the box

        xvalue = (bbox_list[0] + bbox_list[2])/2 #finds the midpoint of the xvalue
        yvalue = (bbox_list[1] + bbox_list[3])/2
            
        position = convertFace(xvalue,yvalue) #convert coordinates to a position in frame
        return position

def checkFace(position,image):
    #tells the user the location of their face and asks if that position is ok
    print(position)
    voice_out("Your face is" + position + ". Would you like to change the position?")
    if voice_in():
        voice_out("What would you like the position to be")
        rePosFace(voice_in())
    else:
        voice_out("Done")
        voice_in()
        cv.imwrite("Final.jpg", image) #saves the image under the name Final in a jpeg format
        cv.imshow("Final",image) #displays the final image, is this needed as user may be completely blind??
        voice_out("Image Saved")

def processObjs(image):
    #initializing lists for positioning
    names = []
    objs = []
    coords = []
    results = model(image) #runs the object detection model on image taken
    names = model.names

    #stores objects detected and their placements in lists
    for r in results:
        boxes = r.boxes #put bounding box detections into a list
        coords.append(boxes.xyxy) #list of the xy coordiantes, first coord is bottom left and second is top right

        for c in r.boxes.cls:
            objs.append(names[int(c)]) #adds name of each object detected to list in same order as coordinates

    numObjs = len(objs)
    count = 0
    coords2 = coords[0] #gets the tenosr that is at the first element of the list

    while count < numObjs:
        #go through each object detected and tell the user what it is and where it is located
        obj = objs[count]
        curcoord = coords2[count,:] #gives the coords of the current object
    
        xvalues = (curcoord[0] + curcoord[2])/2 #adds the start x to the width of the bounding box and divides by 2 to find the midpoint
        yvalues = (curcoord[1] + abs(curcoord[1] - curcoord[3])) #adds the start y to the starting point minus the total height to find the midpoint on the y-axis

        xvalues = xvalues.numpy() #converts from tensor number to numpy number
        yvalues = yvalues.numpy()

        position = convertPos(xvalues,yvalues)
    
        #debugging print statments
        print(obj)
        print(curcoord)
        print(xvalues)
        print(yvalues)
        print(position)
        print(" ")
        count += 1
        checkObj(obj,position,image)

def checkObj(obj, position, image):
    #tells the user the current position of the object and asks if that location is correct
    voice_out("The" + obj + "is" + position + ". Would you like to change the position?")
    if voice_in():
        #user wants to change the position of the current object
        voice_out("What would you like the position to be")
        rePosObj(voice_in())
    else:
        voice_out("Done")
        cv.imwrite("Final.jpg", image) #saves the image under the name Final in a jpeg format
        cv.imshow("Final",image) #displays the final image, is this needed as user may be completely blind??

def rePosObj(gPos, curPos,obj):
    
    while(gPos != curPos):
    #while the current postion of the object does not match the psotion the user wants it to be in
        if(gPos == 'tr'):
            match curPos:
                case "br":
                    print(" Move " + obj + " Up ")
                    time.sleep(3) #makes program waith 3 seconds
                case "tl":
                    print("Move" + obj + "right")
                    time.sleep(3)
                case "bl":
                    print("Move" + obj + "up and right")
                    time.sleep(3)
                case "center":
                    print("Move" + obj + "right")
                    time.sleep(3)
                case "np":
                    print("Move" + obj +  "down and left")
                    time.sleep(3)
        elif(gPos == 'tl'):
            match curPos:
                case 'bl':
                    print("Move" + obj + "up")
                    time.sleep(3)
                case 'tr':
                    print("Move" + obj + "left")
                    time.sleep(3)
                case 'br':
                    print("Move" + obj + "up and left")
                    time.sleep(3)
                case "center":
                    print("Move" + obj + "left")
                    time.sleep(3)
                case "np":
                    print("Move" + obj + "down and right")
                    time.sleep(3)
        elif(gPos == 'br'):
            match curPos:
                case 'tr':
                    print("Move" + obj +"down")
                    time.sleep(3)
                case 'bl':
                    print("Move" + obj + "right")
                    time.sleep(3)
                case 'tl':
                    print("Move" + obj + "down and right")
                    time.sleep(3)
                case 'center':
                    print("Move" + obj +"right")
                    time.sleep(3)
                case 'np':
                    print("Move" + obj + "up and left")
                    time.sleep(3)
        elif (gPos == "bl"):
            match curPos:
                case 'tl':
                    print("Move" + obj + "down")
                    time.sleep(3)
                case 'br':
                    print("Move" + obj +"left")
                    time.sleep(3)
                case 'tr':
                    print("Move" + obj + "down and left")
                    time.sleep(3)
                case 'center':
                    print("Move" + obj + "left")
                    time.sleep(3)
                case 'np':
                    print("Move" + obj + "up and right")
                    time.sleep(3)
        elif gPos == 'center':
            match curPos:
                case 'bl':
                    print("Move" + obj + "right")
                    time.sleep(3)
                case 'tl':
                    print("Move" + obj +  "right")
                    time.sleep(3)
                case 'tr':
                    print("Move" + obj + "left")
                    time.sleep(3)
                case 'br':
                    print("Move" + obj + "left")
                    time.sleep(3)
        
        #retakes the photo and processes it to find the new postion
        image = take_photo()
        coords = processFace(image) 
        curPos = convertFace(coords[0],coords[1])
        print("Your current position is: ", curPos)

    #save the image when object is in the correct postion
    cv.imshow("Fianl",image)
    cv.imwrite("Final.jpg",image)

def rePosFace(gPos, curPos):
    while(gPos != curPos):
    #while the face is not in the part of the image that the user wants it in give instructions based on the goal position
        if(gPos == 'tr'):
            match curPos:
                case "br":
                    print("Move face Up")
                    time.sleep(3) #makes program waith 3 seconds
                case "tl":
                    print("Move face right")
                    time.sleep(3)
                case "bl":
                    print("Move face up and right")
                    time.sleep(3)
                case "center":
                    print("Move face right")
                    time.sleep(3)
                case "np":
                    print("Move face down and left")
                    time.sleep(3)
        elif(gPos == 'tl'):
            match curPos:
                case 'bl':
                    print("Move face up")
                    time.sleep(3)
                case 'tr':
                    print("Move face left")
                    time.sleep(3)
                case 'br':
                    print("Move face up and left")
                    time.sleep(3)
                case "center":
                    print("Move face left")
                    time.sleep(3)
                case "np":
                    print("Move face down and right")
                    time.sleep(3)
        elif(gPos == 'br'):
            match curPos:
                case 'tr':
                    print("Move face down")
                    time.sleep(3)
                case 'bl':
                    print("Move face right")
                    time.sleep(3)
                case 'tl':
                    print("Move face down and right")
                    time.sleep(3)
                case 'center':
                    print("Move face right")
                    time.sleep(3)
                case 'np':
                    print("Move face up and left")
                    time.sleep(3)
        elif (gPos == "bl"):
            match curPos:
                case 'tl':
                    print("Move face down")
                    time.sleep(3)
                case 'br':
                    print("Move face left")
                    time.sleep(3)
                case 'tr':
                    print("Move face down and left")
                    time.sleep(3)
                case 'center':
                    print("Move face left")
                    time.sleep(3)
                case 'np':
                    print("Move face up and right")
                    time.sleep(3)
        elif gPos == 'center':
            match curPos:
                case 'bl':
                    print("Move face right")
                    time.sleep(3)
                case 'tl':
                    print("Move face right")
                    time.sleep(3)
                case 'tr':
                    print("Move face left")
                    time.sleep(3)
                case 'br':
                    print("Move face left")
                    time.sleep(3)
        
        #take a new photo and process it to find the new current position of the face
        image = take_photo()
        coords = processFace(image) 
        curPos = convertFace(coords[0],coords[1])
        print("Your current position is: ", curPos)

    #save the image when it is in the correct section as specified by the user
    cv.imshow("Fianl",image)
    cv.imwrite("Final.jpg",image)

def convertPos(x,y):
     #take the coord and make it an accepted postion
    
    if(((x < 240) and (y < 320))):
        pos = "bl" #center of object is in bottom left, as x and y positons are less than edges
    elif(((x < 240 ) and (y > 320))):
        pos = "tl" #center of object is in top left as x value is less than horizontal bound and y is greater than vertical bound
    elif (((x > 400) and (y < 320))):
        pos = "br" #in bottom right
    elif(((x > 400) and (y > 320))):
        pos = "tr" #in top right
    elif((x > 240) and (x <400)):
        pos = "center" #temporary default
    else:
        pos = "Not in a position"
    #currently no case for the center being on a line or object is in multiple sections

    return pos

def convertFace(x,y):
    #takes the coord of the midpoint and make it an accepted postion
    
    if(((x < .24) and (y > .320))):
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
        pos = "Not in a position"
    #currently no case for the center being on a line or object is in multiple sections

    return pos

if __name__ == "__main__":
    main()