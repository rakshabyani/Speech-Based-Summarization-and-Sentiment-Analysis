import csv
import pickle
from emotionCodes import *
from dataLocations import dataParameters
from utils import *

data={}
fileInfo = {}


def getFiles(path):
    return os.listdir(path)

def getFileInfo(file,path):
    global fileInfo
    tokens = []
    timelines = []
    try:
        with open(path + file) as f:
            reader = csv.reader(f, delimiter="\t")
            for line in reader:
                #line=str(line).rstrip().lstrip().split("\t")
                tokens.append(line[1])
                timelines.append(float(line[0]))
        if tokens and timelines:
            filedata={}
            filedata["emotion"]=emotionCodes.getEmotion(file[5])
            filedata["tokens"]=tokens
            filedata["timeFragments"]=timelines
            fileInfo[file.split(".")[0]]=filedata
    except Exception as e:
        print "In catch: "+file+" with error: "+e.message

def processData():
    try:
        path = dataParameters.getPath("silb")
    except NameError as e:
        print e.message
    files=getFiles(path)
    for fileName in files:
        getFileInfo(fileName,path)
    print fileInfo

def writeSilbData():
    fileName=dataParameters.getFile("silbData")
    filepath=dataParameters.getPath("modelResults")
    if not checkDirExistance(filepath+fileName) :
        createDir(filepath+fileName)
    with open(filepath+fileName,"w") as f:
        pickle.dump(fileInfo,f)


processData()
writeSilbData()
