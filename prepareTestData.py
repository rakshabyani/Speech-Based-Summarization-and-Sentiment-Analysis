from utils import *
import json
import codecs
from collections import Counter
from pydub import AudioSegment
from dataLocations import dataParameters
from featureExtractor import getFeatures,reshapeArraysForSentences
import pandas as pd
from summariser import sentenceTokeniser
from utils import *
from classify import predict_emotion, classify
import matplotlib.pyplot as plt

stopwords = [",","\"","-",":",";",".","&","!","?"]

def createTimeFrames(audioPath, transcriptPath):
    '''
    @createTimeFrame creates a json with time frames by aligning the text from transcript and token from audio
    :param path: path containing the wav and transcript files
    :return:
    '''
    #path = "./testData/"
    #for files in listFiles(path):
    filename = getFileName(transcriptPath)
    extension = transcriptPath.split(".")[-1]
    filepathWithName = "."+audioPath.split(".")[1]
    data = sentenceTokeniser(open(transcriptPath,"r").read())
    print data
    with codecs.open(transcriptPath,"w",encoding="utf-8") as f:
        for line in data:
            #line = ' '.join([word for word in line.split() if word not in stopwords])
            #for word in line.split():
            f.write(line+"\n")
    cmd = "python -m aeneas.tools.execute_task "+ audioPath + " " + transcriptPath +" \"task_language=deu|os_task_file_format=aud|is_text_type=plain\" "+filepathWithName+".json"
    print cmd
    execute(cmd)



### check json
def createFragments(jsonfilePath,audiofilePath,outputPath):
    '''
    @createFragments segments the audio file based on time frames
    :param inputPath: path containing wav file
    :param filename: name of the file
    :param outputPath: output path
    :return:
    '''
    '''
    sound = AudioSegment.from_mp3(filename)
    [file, extension] = filename.split(".")
    with open(inputPath+file+".json") as f:
        data=f.readlines()
    print data,len(data)
    for fragment in data:
        fragment = fragment.split("\t")
        w=sound[float(fragment[0])*1000:float(fragment[1])*1000]
        print "exporting data wave "+fragment[2]
        w.export(outputPath+file+".wav", format="wav")'''

    sound = AudioSegment.from_mp3(audiofilePath)
    filename = getFileName(audiofilePath)
    with open(jsonfilePath) as f:
        data = f.readlines()
    print data, len(data)
    filepathWithName = "."+audiofilePath.split(".")[1]
    i=0
    testSoundPath = "./testData/tokens/"
    tokenEmotions = []
    for fragment in data:
        df = pd.DataFrame(columns=(
        'F0', 'spectralCentroid', 'MFCC', 'energy', 'chroma', 'spectralFlux', 'spectralSpread', 'spectralEntropy',
        'ZCR', 'loudness', 'energyEntropy', 'chromaDeviation', 'spectralRolloff'))
        fragment = fragment.split("\t")
        w = sound[float(fragment[0]) * 1000:float(fragment[1]) * 1000]
        print "exporting data wave " + fragment[2]
        w.export(testSoundPath+filename + str(i) + ".wav", format="wav")
        try:
            val = getFeatures(testSoundPath+filename + str(i)+".wav")
            val = reshapeArraysForSentences(val)
            df.loc[0] = val.values()
            df.to_csv("sample.csv")
            print df
            emotions = predict_emotion(df.loc[0])
            emotions = Counter(emotions)
            tokenEmotions.append(fragment[2]+"/"+emotions.most_common()[0]+"\n")
            print tokenEmotions[-1]
        except Exception as e:
            print "Error in method with message: ", e.message
        i+=1


#createTimeFrames()
#createFragments() #give parameters
#buildTestModelForTokens()
classify()
createTimeFrames("./testData/test.mp3","./testData/test.txt")
createFragments("./testData/test.json","./testData/test.mp3","")


#df = pd.read_csv("./results/models/averageValues.csv")
#print df[['energy']]
#plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy');
