from utils import *
import json
from pydub import AudioSegment
from dataLocations import dataParameters
from featureExtractor import computeAvg, getFeatures,reshapeArrays, computeTotal
import pandas as pd
from summariser import sentenceTokeniser


def createTimeFrames(path):
    '''
    @createTimeFrame creates a json with time frames by aligning the text from transcript and token from audio
    :param path: path containing the wav and transcript files
    :return:
    '''
    #path = "./testData/"
    for files in listFiles(path):
        [filename, extension] = files.split(".")
        data = sentenceTokeniser(open(path+filename+".txt","r").read())
        with open(path+filename+".txt","w") as f:
            f.write(data)
        if "wav" not in extension:
            cmd = "python -m aeneas.tools.execute_task "+ path+files + " " + path+filename +".txt \"task_language=deu|os_task_file_format=aud|is_text_type=plain\" "+path+filename+".json"
            print cmd
            execute(cmd)



### check json
def createFragments(inputPath,filename,outputPath):
    '''
    @createFragments segments the audio file based on time frames
    :param inputPath: path containing wav file
    :param filename: name of the file
    :param outputPath: output path
    :return:
    '''
    sound = AudioSegment.from_mp3(filename)
    [file, extension] = filename.split(".")
    with open(inputPath+file+".json") as f:
        data=json.load(f)['fragments']
    print data,len(data)
    for fragment in data:
        w=sound[float(fragment['begin'])*1000:float(fragment['end'])*1000]
        print "exporting data wave "+fragment['lines'][0]
        w.export(outputPath+file+".wav", format="wav")


def getDataFrame(filePath):
    '''
    @getDataFrame creates a model for each emotion in the fragment folder
    :param filePath: folder containing sound fragments for different emotions
    :param emotion: emotion name
    :return: model for the emotion as pandas Data Frame
    '''
    df = pd.DataFrame(columns=('F0', 'spectralCentroid', 'MFCC', 'energy', 'chroma', 'spectralFlux', 'spectralSpread', 'spectralEntropy', 'ZCR', 'loudness', 'energyEntropy', 'chromaDeviation', 'spectralRolloff'))
    avg_dict={}
    path = filePath
    for filename in listFiles(path):
        try:
            val = getFeatures(path+"/"+filename)
            val = reshapeArrays(val)
            avg_dict = computeTotal(val,avg_dict)
            df.loc[filename.split(".")[0]] = val.values()
        except Exception as e:
            print filename, e.message
    avg_dict = computeAvg(avg_dict,df.shape[0])
    return df, avg_dict

def buildTestModelForTokens(wavPath):
    '''
    @buildModel builds the model for each emotion
    :return:
    '''
    path = wavPath
    modelPath = dataParameters.getPath("testModelResults")   ##chanage path
    if not checkDirExistance(modelPath):
        try:
            createDir(modelPath)
        except OSError as e:
            print "Error in build model while creating directory with message: ", e.message
    avg_df = pd.DataFrame(columns=(
    'F0', 'spectralCentroid', 'MFCC', 'energy', 'chroma', 'spectralFlux', 'spectralSpread', 'spectralEntropy', 'ZCR',
    'loudness', 'energyEntropy', 'chromaDeviation', 'spectralRolloff'))
    for folder in listFiles(path):
        df,avg_dict = getDataFrame(path,folder)
        print df
        avg_df.loc[folder] = avg_dict.values()
        open(modelPath+folder+".csv",'a').close()
        open(modelPath + folder + ".pkl", 'a').close()
        df.to_pickle(modelPath+folder+".pkl")
        df.to_csv(modelPath+folder+".csv")
    #open(modelPath + "averageValues.csv", 'a').close()
    #avg_df.to_csv(modelPath + "averageValues.csv")
    #open(modelPath + "averageValues.csv", 'a').close()
    #avg_df.to_pickle(modelPath + "averageValues.pkl")
    return

#createTimeFrames()
#createFragments() #give parameters
#buildTestModelForTokens()
