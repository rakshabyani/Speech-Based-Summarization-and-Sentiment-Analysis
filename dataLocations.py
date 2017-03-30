'''
@dataParameters class contains information about the path locations and the file names used in the project
'''
class dataParameters(object):
    filePaths = {"silb" : "./emoDB/silb/", "wav": "./emoDB/wav/", "wavTargets": "./fragmentedAudio/", "modelResults":"./results/"}
    fileNames = {"silbData":"silbData.pkl"}

    '''
    @getPath takes the path codes and returns the path else throws an Exception
    Parameters
    ----------
        code : String

    '''
    @classmethod
    def getPath(cls,code):
        if cls.filePaths.has_key(code):
            return cls.filePaths[code]
        raise NameError("No such location")

    '''
        @getFile takes the name of the file as codes and returns the file name else throws an Exception
        Parameters
        ----------
            code : String

        '''
    @classmethod
    def getFile(cls,file):
        if cls.fileNames.has_key(file):
            return cls.fileNames[file]
        raise NameError("No such file")