import speech_recognition as sr

r = sr.Recognizer()

def record_text():
    """Records audio input and returns the transcribed text."""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return None
        except sr.UnknownValueError:
            print("Unknown error. Please try speaking again.")
            return None
