from pydub import AudioSegment
from dataLocations import dataParameters
import pickle
import os
with open("silbData.pkl") as f:
    data = pickle.load(f)

def createDir(path):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

for file in data:
    sound = AudioSegment.from_mp3(dataParameters.getPath("wav")+file+"wav")
    timeline = file["timeFragments"]
    print sound.duration_seconds
    # len() and slicing are in milliseconds
    start = timeline[0]
    i=1
    while i<len(timeline):
        w=sound[start*1000:timeline[i]*1000]
        print "exporting data wave "+ str(i)
        filename = dataParameters.getPath("wavTargets")+file+str(i-1)+".wav"
        if not os.path.exists(os.path.dirname(dataParameters.getPath("wavTargets"))):
            createDir(filename)
        else:
            w.export(filename, format="wav")
        start=timeline[i]
        i+=1


