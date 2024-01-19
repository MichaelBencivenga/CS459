import pyttsx3
try:
    engine = pyttsx3.init
except:
    print("oops")
    
#false = selfie true = subject
#Could we have the spacebar interupt the program at any time and allow for command input? Or just something to allow user input at any time?
cameramode = False
def main():
    try:        
        #engine.onError(voice_output, "VoiceError")
        engine.setProperty('volume', 0.5)
        voice_out("Hello welcome to the program, would you like to change the volume?")
        cvol = False #change volume
        if voice_in:
            cvol = True
        while cvol == True:
            voice_out("what would you like the volume set to out of 100?")
            volume = voice_in
            engine.setProperty('volume', volume)
            voice_out("Is this volume good?")
            if voice_in:
                cvol = False
        voice_out("Would you like to take a selfie or photograph an object?")
        voice_in()
    except Exception:
        print(Exception)
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
                take_photo()
            case "object":
                cameramode = 1
                take_photo()
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
def voice_in():
    #Start voice input
    vo_in =  "" #convert voice to string
    return vo_in
def voice_out(vo_out):
    engine.say(vo_out)
    engine.runAndWait()
def take_photo():
    voice_out("Ready for photo?")
    #Take a little silly photo
    if cameramode == 0:
        position = 1 #get position
        voice_out("Your face is" + position + ". Would you like to change the position?")
        if commands(voice_in_in()) == True:
            voice_out("What would you like the position to be")
            reposition(voice_in())
        else:
            voice_out("Done")
def reposition(posw):
    #Position wanted
    #Numbers are in no way shape or form final but this was my idea of how to interpret it
    #could probably go more in depth like allowing center top right. Nothing coming to mind rn though
    posc = (0,0) #change to grab from api
    match position:
        case "center":
            posw = (0,0)
        case "bl":
            posw = (-5,-5)
        case "br":
            posw = (5,-5)
        case "tl":
            posw = (-5,5)
        case "tr":
            posw = (5,5)
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