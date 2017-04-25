'''
@dataParameters class contains information about the path locations and the file names used in the project
'''
class dataParameters(object):
    filePaths = {"silb": "./emoDB/silb/", "wav": "./emoDB/wav/", "wavTargets": "./fragmentedAudio/", "results": "./results/", "modelResults": "./results/models/tokenModel/", "wavSentences": "./sentencesAudio/", "sentenceModel": "./results/models/sentenceModels/"}
    fileNames = {"silbData": "silbData.pkl"}

    @classmethod
    def getPath(cls,code):
        '''
        @getPath takes the path codes and returns the path else throws an Exception
        :param code: key from dictionary for the path
        :return: path
        '''
        if cls.filePaths.has_key(code):
            return cls.filePaths[code]
        raise NameError("No such location")

    @classmethod
    def getFile(cls,file):
        '''
        @getFile takes the name of the file as codes and returns the file name else throws an Exception
        :param file: key from dictionary for the file
        :return: file name
        '''
        if cls.fileNames.has_key(file):
            return cls.fileNames[file]
        raise NameError("No such file")