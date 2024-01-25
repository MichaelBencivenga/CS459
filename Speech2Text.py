import speech_recognition as sr


def get_user_input():
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        print(
            "Please state your command..."
        )  # this can be changed to use text to speech for blind users
        audio = r.listen(source, timeout=10, phrase_time_limit=3)
        text = r.recognize_google(audio)
        return text
