class dataParameters():
    filePaths = {"silb" : "./emoDB/silb/", "wav": "./emoDB/wav/", "wavTargets": "./fragmentedAudio/"}

    def getPath(code):
        if filePaths.has_key(code):
            return filePaths[code]
        return None