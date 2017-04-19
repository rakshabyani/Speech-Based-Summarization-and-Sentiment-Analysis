import speech_recognition as sr


# Speech recognition using Google Speech Recognition


def speechToText(f):
    try:
        r = sr.Recognizer()
        with sr.AudioFile(f) as source:
            audio = r.listen(source)
            transcript = r.recognize_google(audio, language="de_DE")
            return transcript
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
