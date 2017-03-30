import os
def createDir(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc:  # Guard against race condition
        raise

def checkDirExistance(path):
    return os.path.exists(path)