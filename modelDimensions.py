class modelDimensions(object):
    dimensionCodes = {"spectralCentroid": (1,65), "MFCC": (12,65), "energy": (1,65), "chroma": (10,65), "spectralFlux": (1,65), "spectralSpread": (1,65),
                    "spectralEntropy": (1,65) ,"ZCR": (1,65), "energyEntropy": (1,65),"chromaDeviation": (1,65),"spectralRolloff":(1,65),"F0":(1,1),"loudness": (1,1)}
    sentenceDimensionCodes = {"spectralCentroid": (1, 500), "MFCC": (12, 500), "energy": (1, 500), "chroma": (10, 500),
                      "spectralFlux": (1, 500), "spectralSpread": (1, 500),
                      "spectralEntropy": (1, 500), "ZCR": (1, 500), "energyEntropy": (1, 500), "chromaDeviation": (1, 500),
                      "spectralRolloff": (1, 500), "F0": (1, 1), "loudness": (1, 1)}

    @classmethod
    def getDimension(cls,code):
        '''
        @getEmotion returns the emotion name for the given code
        :param code: emotion code
        :return: emotion
        '''
        if cls.dimensionCodes.has_key(code):
            return cls.dimensionCodes[code]
        return None

    @classmethod
    def getSentenceDimension(cls, code):
        '''
        @getEmotion returns the emotion name for the given code
        :param code: emotion code
        :return: emotion
        '''
        if cls.sentenceDimensionCodes.has_key(code):
            return cls.sentenceDimensionCodes[code]
        return None
