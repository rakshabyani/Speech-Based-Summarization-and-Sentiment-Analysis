import os
import csv
import pickle

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
            filedata["emotion"]=file[5]
            filedata["tokens"]=tokens
            filedata["timeFragments"]=timelines
            fileInfo[file.split(".")[0]]=filedata
    except Exception:
        print "In catch: "+file

path="./emoDB/silb/"
files=getFiles(path)
for file in files:
    getFileInfo(file,path)

print fileInfo

with open("silbData.pkl","w") as f:
    pickle.dump(fileInfo,f)

