from pydub import AudioSegment
from dataLocations import dataParameters
import pickle
from utils import  *

def getsilbData():
    fileName=dataParameters.getFile("silbData")
    filepath=dataParameters.getPath("modelResults")
    with open(filepath+fileName) as f:
        data = pickle.load(f)
    return data

def checkDir(path):
    if not checkDirExistance(path):
        createDir(path)
    return

def segmentAudio(data):
    for file in data:
        sound = AudioSegment.from_mp3(dataParameters.getPath("wav")+file+".wav")
        timeline = data[file]["timeFragments"]
        print sound.duration_seconds
        # len() and slicing are in milliseconds
        start = timeline[0]
        i=1
        emotion = data[file]["emotion"]
        while i<len(timeline):
            w=sound[start*1000:timeline[i]*1000]
            print "exporting data wave "+ str(i)
            filename = dataParameters.getPath("wavTargets")+ emotion +"/"+ file+str(i-1)+".wav"
            checkDir(dataParameters.getPath("wavTargets")+ emotion + "/")
            w.export(filename, format="wav")
            start=timeline[i]
            i+=1

model = getsilbData()
segmentAudio(model)