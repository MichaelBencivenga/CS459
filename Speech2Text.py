import speech_recognition as sr


def get_user_input():
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        audio = r.listen(source, timeout=10, phrase_time_limit=3)
        text = r.recognize_google(audio)
        return text
