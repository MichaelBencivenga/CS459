#false = selfie true = subject
cameramode = False
def main():
    print("hello")
    #check libraries are working
    #not this exactly but something similar, grab name of non-working library
    if library == 0:
        error = library + "is being a little silly"
        print(error)
    else:
        voice_out("Would you like to take a selfie or photograph an object?")
        vo_in = user_in()
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
            case _:
                print("Nuh uh")
def user_in():
    #Start voice input
    vo_in =  "" #convert voice to string
    return vo_in
def voice_out(vo_out):
    #use silly api to text to speech 
    print("something so this doesnt have an error")
def take_photo():
    voice_out("Ready for photo?")
    #Take a little silly photo
    if cameramode == 0:
        position = 1 #get position
        voice_out("Your face is" + position + ". Would you like to change the position?")
        vo_in = user_in() 
        