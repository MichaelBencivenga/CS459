import pyttsx3
import time
import cv2 as cv
import ultralytics
from ultralytics import YOLO
from PIL import Image
ultralytics.checks()

global engine
engine = pyttsx3.init()
engine.setProperty('volume', 0.6)

def voice_out(vo_out):
    engine.say(vo_out)
    engine.runAndWait()

def take_image():
    #setting up camera and taking pic
    cam_port =0;
    cam = cv.VideoCapture(cam_port);
    result,image = cam.read();
    image = cv.flip(image,1) #flips image horizonally

    if result: 
        cv.imwrite("testpic.jpg",image);
        return image
    else:
        print("No image detected");


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

def processObjs(image):

    #load a pretrained model
    model = YOLO("yolov8n.pt")

    #use the model
    results = model(image) #predict on an image
    names = model.names #gets the names of the objects detected in the image

    objs = []
    coords = []

    for r in results:
        im_array = r.plot() #plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[...,::-1]) #RGB PIL image

    im.write("AnnotatedIm.jpg")

    boxes = r.boxes #put bounding box detections into a list
    coords.append(boxes.xywh) #list of the xy coordiantes, first coord is bottom left and second is top right

    for c in r.boxes.cls:
        objs.append(names[int(c)]) #adds name of each object detected to list in same order as coordinates

    #numObjs = len(objs)
    count = 0
    coords2 = coords[0] #gets the tenosr that is at the first element of the list

    #while count < numObjs:
        #go through each object detected and tell the user what it is and where it is located
    obj = objs[0]
    curcoord = coords2[count,:] #gives the coords of the current object
    
    xvalues = (curcoord[0] + curcoord[2])/2 #adds the start x to the width of the bounding box and divides by 2 to find the midpoint
    yvalues = (curcoord[1] + abs(curcoord[1] - curcoord[3])) #adds the start y to the height of the bounding box and divides by 2 to find the midpoint

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
        
        #count += 1
    return(xvalues,yvalues)

def reposition (gPos,curPos):
    while(gPos != curPos):
        if(gPos == 'tr'):
            match curPos:
                case "br":
                    voice_out("Move object up")
                    time.sleep(3) #makes program waith 3 seconds
                case "tl":
                    voice_out("Move object right")
                    time.sleep(3)
                case "bl":
                    voice_out("Move object up and right")
                    time.sleep(3)
                case "center":
                    voice_out("Move object right")
                    time.sleep(3)
                case "np":
                    voice_out("Move object down and left")
                    time.sleep(3)
        elif(gPos == 'tl'):
            match curPos:
                case 'bl':
                    voice_out("Move object up")
                    time.sleep(3)
                case 'tr':
                    voice_out("Move object left")
                    time.sleep(3)
                case 'br':
                    voice_out("Move object up and left")
                    time.sleep(3)
                case "center":
                    voice_out("Move object left")
                    time.sleep(3)
                case "np":
                    voice_out("Move object down and right")
                    time.sleep(3)
        elif(gPos == 'br'):
            match curPos:
                case 'tr':
                    voice_out("Move object down")
                    time.sleep(3)
                case 'bl':
                    voice_out("Move object right")
                    time.sleep(3)
                case 'tl':
                    voice_out("Move object down and right")
                    time.sleep(3)
                case 'center':
                    voice_out("Move object right")
                    time.sleep(3)
                case 'np':
                    voice_out("Move object up and left")
                    time.sleep(3)
        elif (gPos == "bl"):
            match curPos:
                case 'tl':
                    voice_out("Move object down")
                    time.sleep(3)
                case 'br':
                    voice_out("Move object left")
                    time.sleep(3)
                case 'tr':
                    voice_out("Move object down and left")
                    time.sleep(3)
                case 'center':
                    voice_out("Move object left")
                    time.sleep(3)
                case 'np':
                    voice_out("Move object up and right")
                    time.sleep(3)
        elif gPos == 'center':
            match curPos:
                case 'bl':
                    voice_out("Move object right")
                    time.sleep(3)
                case 'tl':
                    voice_out("Move object right")
                    time.sleep(3)
                case 'tr':
                    voice_out("Move object left")
                    time.sleep(3)
                case 'br':
                    voice_out("Move object left")
                    time.sleep(3)
        
        image = take_image()
        coords = processObjs(image) 
        curPos = convertPos(coords[0],coords[1])
        #voice_out("Your current position is: ", curPos, "goal: ", gPos)


    image.show("FianlObj",)
    cv.imwrite("FinalObj.jpg",image)


voice_out("Welcome to the program get ready for your static image")
image = take_image()
voice_out("Image taken")
coords = processObjs(image)
position = convertPos(coords[0],coords[1])

goalPos = input("Where would you like the object to be positioned")
print(goalPos)
if position == goalPos:
    cv.imshow("FinalObj",image)
    cv.imwrite("FinalObj.jpg",image)
else:
    reposition(goalPos,position)