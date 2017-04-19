import os

def createDir(path):
    '''to create a directory in the given path
    :param path: path where the directory has to be created
    '''
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc:  # Guard against race condition
        raise

def checkDirExistance(path):
    '''
    check the existance of a directory/file in the given path
    :param path: directory/file to check
    :return: Boolean
    '''
    return os.path.exists(path)

def listFiles(path):
    '''
    list all the directories/files in the given path
    :param path: path
    :return: list of directories and files
    '''
    try:
        return os.listdir(path)
    except OSError as e:
        print "error in getFolders: ",e.message

def getFileName(path):
    '''
    @getFileName is used to get name of the file from given path
    :param path: path to extract the file name
    :return: file name
    '''
    return (path.split("/")[-1]).split(".")[0]
