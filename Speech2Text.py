import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(sample_rate=16000) as source:
    print("Start speaking now...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
        except:
            print("Input not recorded, please try again.")
