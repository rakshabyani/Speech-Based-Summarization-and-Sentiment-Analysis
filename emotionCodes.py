class emotionCodes(object):
    emotionCodes = {"W": "Anger", "L": "Boredom", "E": "Disgust", "A": "Anxiety", "F": "Happiness", "T": "Sadness",
                    "N": "Neutral"}
    @classmethod
    def getEmotion(cls,code):
        '''
        @getEmotion returns the emotion name for the given code
        :param code: emotion code
        :return: emotion
        '''
        if cls.emotionCodes.has_key(code):
            return cls.emotionCodes[code]
        return None
