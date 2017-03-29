from enum import Enum

class emotionCodes():
    emotionCodes = {"W": "Anger", "L": "Boredom", "E": "Disgust", "A": "Anxiety", "F": "Happiness", "T": "Sadness",
                    "N": "Neutral"}

    def getEmotion(code):
        if emotionCodes.has_key(code):
            return emotionCodes[code]
        return None
