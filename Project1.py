#import for speech and text
import pyttsx3 
#imports for taking images and face + object detection
import cv2 as cv
import mediapipe as mp
import ultralytics
#setting up object detection using the ultralytics library and yolov8 model and training set
from ultralytics import YOLO
from PIL import Image
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
    try:
        #engine.onError(voice_output, "VoiceError")
        global engine 
        engine = pyttsx3.init()
        engine.setProperty('volume', 0.5)
        voice_out("Hello welcome to the program, would you like to change the volume?")
        cvol = False #change volume
        if voice_in():
            #change volume
            cvol = True
        while cvol == True:
            voice_out("what would you like the volume set to out of 100?")
            volume = voice_in()
            engine.setProperty('volume', volume)
            voice_out("Is this volume good?")
            if voice_in():
                cvol = False
        voice_out("Would you like to take a selfie or photograph an object?")
        voice_in()
    except Exception as e:
        #Print details of the exception
        print(f"An exception occurred: {type(e).__name__}")
        print(f"Exception details: {e}")

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
        return vo_in / 100
    else:
        match vo_in:
            case "commands":
                #list avalible commands
                voice_out("stored as list")
            case "home":
                #idk about this one
                main()
            case "selfie":
                cameramode = 0
                image = take_photo(cameramode)
                curpos = processFace(image)
                checkFace(curpos,image)
            case "object":
                cameramode = 1
                image = take_photo(cameramode)
                curpos = processObjs(image)
            case "change object": #repeat effect but I felt like we needed the option to change object.
                cameramode = 1
                take_photo(cameramode) 
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


def voice_in(object=0):
    #Start voice input
    #code should not procceed until it gets an input
    vo_in =  input("enter command") #convert voice to string
    if object:
        vo_in
    return commands(vo_in)

def voice_out(vo_out):
    engine.say(vo_out)
    engine.runAndWait()

def take_photo(cameramode):

    if cameramode == 0:
        #Selfie option
        
        voice_out("Are you ready for the selfie?")
        if voice_in() == False:
            voice_out("Say yes when ready")
            voice_in()
            #Take a little silly photo
            #selfie
            image = webcam.read()
            image = cv.flip(image,1) #flips the image horizontally
            
            return image
    else:
        #Object option
        voice_out("Are you ready for the static image?")
        if voice_in() == False:
            voice_out("Say yes when ready")
            voice_in()
            image = webcam.read()
            image = cv.flip(image,1) #flips image horizontally

    return image

def processFace(image):
    image2 = cv.cvtColor(image,cv.COLOR_BGR2RGB) #changes color scale to allow mediapipe image processing
    results = mp_face_detection.process(image) #uses face detection model to find faces in image
    image2 = cv.cvtColor(image,cv.COLOR_RGB2BGR) #return image to original color scale

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
    voice_out("Your face is" + position + ". Would you like to change the position?")
    if voice_in():
        voice_out("What would you like the position to be")
        reposition(voice_in())
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
        reposition(voice_in())
    else:
        voice_out("Done")
        cv.imwrite("Final.jpg", image) #saves the image under the name Final in a jpeg format
        cv.imshow("Final",image) #displays the final image, is this needed as user may be completely blind??


def reposition(posw):
    #should probably make one for objects and one for face beceause they are processed differently
    #could just be a while loop that takes pics processes them and gives directions until current position and the goal position match
    #Position wanted
    #Numbers are in no way shape or form final but this was my idea of how to interpret it
    #could probably go more in depth like allowing center top right. Nothing coming to mind rn though
    screenr = (640,640) #grab from api
    posc = (0,0) #change to grab from api, position current
    position = voice_in()
    match position:
        case "center":
            posw = (screenr[0]/2,screenr[1]/2)
        case "bl":
            posw = (screenr[0]*0.25,screenr[1]*0.25)
        case "br":
            posw = (screenr[0]*0.75,screenr[1]/0.25)
        case "tl":
            posw = (screenr[0]*0.25,screenr[1]*0.75)
        case "tr":
            posw = (screenr[0]*0.75,screenr[1]*0.75)
        case _:
            print("Nuh uh")
    while posc != posw:
        if posw[0] != posc[0]:
            if posw[0] < posc[0]:
                voice_out("down")
            else:
                voice_out("up")
        if posw[1] != posc[1]:
            if posw[1] < posc[1]:
                voice_out("left")
            else:
                voice_out("right")

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