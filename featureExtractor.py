from pyAudioAnalysis import audioBasicIO, audioFeatureExtraction
import matplotlib.pyplot as plt
from matplotlib.mlab import find
from dataLocations import dataParameters
from modelDimensions import modelDimensions
import numpy as np
import math
import pandas as pd
from utils import *

def getPitch(signal,Fs):
    '''
    @getPitch calculates the F0 of the sound fragment
    :param signal: sound fragment
    :param Fs: sound sampling rate
    :return: F0 value
    '''
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0 = round(len(index) *Fs /(2*np.prod(len(signal))))
    return f0

def getRMS(sound):
    '''
    @getRMS calculates the average loudness of the sound fragment
    :param sound: sound fragment
    :return: rms value (loudness)
    '''
    n = len(sound)
    #rms_signal = numpy.zeros(n)
    rms_signal = math.sqrt(sum([s**2 for s in sound])/n)
    return rms_signal
'''
n = len(interval)
    rms_signal = numpy.zeros(n)
    for i in range(n):
        small_index = max(0, i - halfwindow)  # intended to avoid boundary effect
        big_index = min(n, i + halfwindow)    # intended to avoid boundary effect
        window_samples = interval[small_index:big_index]

        # here is the RMS of the window, being attributed to rms_signal 'i'th sample:
        rms_signal[i] = sqrt(sum([s**2 for s in window_samples])/len(window_samples))

    return rms_signal
'''

def getFeatures(filePath):
    '''
    @getFeatures extracts different features like F0, Energy, Loudness, Chromograms etc. from the given sound
    :param filePath: path of the sound file
    :return: dict of features
    '''
    values={}
    [Fs, x] = audioBasicIO.readAudioFile(filePath)
    F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050 * Fs, 0.025 * Fs)
    values['F0'] = np.array([getPitch(x,Fs)], dtype=np.float64)
    values['loudness'] = np.array([getRMS(x)], dtype=np.float64)
    values['ZCR'] = F[0] #Zero Crossing Rate
    values['energyEntropy'] = F[2] #Entropy of Energy
    values['spectralCentroid'] = F[3] #Spectral Centroid
    values['spectralSpread'] = F[4] #Spectral Spread
    values['spectralEntropy'] = F[5] #Spectral Entropy
    values['spectralFlux'] = F[6] #Spectral Flux
    values['spectralRolloff'] = F[7] #Spectral Rolloff
    values['MFCC'] = F[8:20] #MFCCs
    values['energy'] = F[1,:] #energy
    values['chroma'] = F[22:32]  #Chroma Vector
    values['chromaDeviation'] = F[33] #Chroma Deviation
    return values

def getNewArray(shape):
    '''
    @getNewArray creates new numpy array of specified shape
    :param shape: new shape of array
    :return: new array with desired shape
    '''
    return np.zeros(shape=shape, dtype=np.float64)

def copyData(oldMatrix, newMatrix):
    '''
    @copyData copies values to new Matrix
    :param oldMatrix: old numpy matrix
    :param newMatrix: new numpy matrix with new dimensions
    :return: new matrix with data
    '''
    (rows, column) = (None, None)
    try:
        (rows, column) = oldMatrix.shape
    except Exception as e:
        x = oldMatrix.shape
        oldMatrix = np.reshape(oldMatrix,(1,x[0]))
        (rows, column) = oldMatrix.shape
    finally:
        for i in xrange(rows):
            newMatrix[i,:column] = oldMatrix[i,:]
    return newMatrix

def reshapeArrays(features):
    '''
    @reshapeArrays reshapes the feature arrays as per specifications to create a generalised model
    :param features: feature dictionary
    :return: feature dictionary with reshaped arrays
    '''
    newFeatureDict = {}
    for feature in features.keys():
        newMatrix = getNewArray(modelDimensions.getDimension(feature))
        if feature == 'loudness' or feature == 'F0':
            newMatrix = features[feature]
        else:
            newMatrix = copyData(features[feature], newMatrix)
        newFeatureDict[feature] = newMatrix
    return newFeatureDict

def computeTotal(features,avg_Dict):
    '''
    @computeTotal computes the sum values for an emotion type
    :param features: feature values
    :param avg_Dict: dictionary containing sum of vectors/matrix
    :return: dictionary containing sum of values/matrix
    '''
    if avg_Dict:
        for feature in features:
            avg_Dict[feature] = np.add(avg_Dict[feature],features[feature])
    else:
        avg_Dict = features
    return avg_Dict


def reshapeArraysForSentences(features):
    '''
    @reshapeArrays reshapes the feature arrays as per specifications to create a generalised model
    :param features: feature dictionary
    :return: feature dictionary with reshaped arrays
    '''
    newFeatureDict = {}
    for feature in features.keys():
        newMatrix = getNewArray(modelDimensions.getSentenceDimension(feature))
        if feature == 'loudness' or feature == 'F0':
            newMatrix = features[feature]
        else:
            newMatrix = copyData(features[feature], newMatrix)
        newFeatureDict[feature] = newMatrix
    return newFeatureDict


def computeTotalSentences(features,avg_Dict):
    '''
    @computeTotal computes the sum values for an emotion type
    :param features: feature values
    :param avg_Dict: dictionary containing sum of vectors/matrix
    :return: dictionary containing sum of values/matrix
    '''
    if avg_Dict:
        for feature in features:
            avg_Dict[feature] = np.add(avg_Dict[feature],features[feature])
    else:
        avg_Dict = features
    return avg_Dict


def computeAvg(avg_dict,n):
    #e / e.sum(axis=1)[:, None]
    for feature in avg_dict.keys():
        if feature == 'loudness' or feature == 'F0':
            avg_dict[feature] = avg_dict[feature]/n
        else:
            avg_dict[feature] = avg_dict[feature] / avg_dict[feature].sum(axis=1)[:, None]
    return avg_dict


def getDataFrameForSentences(filePath,emotion):
    '''
    @getDataFrame creates a model for each emotion in the fragment folder
    :param filePath: folder containing sound fragments for different emotions
    :param emotion: emotion name
    :return: model for the emotion as pandas Data Frame
    '''
    df = pd.DataFrame(columns=('F0', 'spectralCentroid', 'MFCC', 'energy', 'chroma', 'spectralFlux', 'spectralSpread', 'spectralEntropy', 'ZCR', 'loudness', 'energyEntropy', 'chromaDeviation', 'spectralRolloff'))
    avg_dict={}
    path = filePath+emotion
    for filename in listFiles(path):
        try:
            val = getFeatures(path+"/"+filename)
            val = reshapeArraysForSentences(val)
            avg_dict = computeTotalSentences(val,avg_dict)
            df.loc[filename.split(".")[0]] = val.values()
        except Exception as e:
            print filename, emotion, e.message
    avg_dict = computeAvg(avg_dict,df.shape[0])
    return df, avg_dict


def getDataFrame(filePath,emotion):
    '''
    @getDataFrame creates a model for each emotion in the fragment folder
    :param filePath: folder containing sound fragments for different emotions
    :param emotion: emotion name
    :return: model for the emotion as pandas Data Frame
    '''
    df = pd.DataFrame(columns=('F0', 'spectralCentroid', 'MFCC', 'energy', 'chroma', 'spectralFlux', 'spectralSpread', 'spectralEntropy', 'ZCR', 'loudness', 'energyEntropy', 'chromaDeviation', 'spectralRolloff'))
    avg_dict={}
    path = filePath+emotion
    for filename in listFiles(path):
        try:
            val = getFeatures(path+"/"+filename)
            val = reshapeArrays(val)
            avg_dict = computeTotal(val,avg_dict)
            df.loc[filename.split(".")[0]] = val.values()
        except Exception as e:
            print filename, emotion, e.message
    avg_dict = computeAvg(avg_dict,df.shape[0])
    return df, avg_dict

def buildModelForTokens():
    '''
    @buildModel builds the model for each emotion
    :return:
    '''
    path = dataParameters.getPath("wavTargets")
    modelPath = dataParameters.getPath("modelResults")
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
    open(modelPath + "averageValues.csv", 'a').close()
    avg_df.to_csv(modelPath + "averageValues.csv")
    open(modelPath + "averageValues.csv", 'a').close()
    avg_df.to_pickle(modelPath + "averageValues.pkl")
    return

def buildModelForSentences():
    '''
    @buildModel builds the model for each emotion
    :return:
    '''
    path = dataParameters.getPath("wavSentences")
    modelPath = dataParameters.getPath("sentenceModel")
    if not checkDirExistance(modelPath):
        try:
            createDir(modelPath)
        except OSError as e:
            print "Error in build model while creating directory with message: ", e.message
    avg_df = pd.DataFrame(columns=(
        'F0', 'spectralCentroid', 'MFCC', 'energy', 'chroma', 'spectralFlux', 'spectralSpread', 'spectralEntropy',
        'ZCR',
        'loudness', 'energyEntropy', 'chromaDeviation', 'spectralRolloff'))
    for folder in listFiles(path):
        df, avg_dict = getDataFrameForSentences(path, folder)
        print df
        avg_df.loc[folder] = avg_dict.values()
        open(modelPath + folder + ".csv", 'a').close()
        open(modelPath + folder + ".pkl", 'a').close()
        df.to_pickle(modelPath + folder + ".pkl")
        df.to_csv(modelPath + folder + ".csv")
    open(modelPath + "averageValues.csv", 'a').close()
    avg_df.to_csv(modelPath + "averageValues.csv")
    open(modelPath + "averageValues.csv", 'a').close()
    avg_df.to_pickle(modelPath + "averageValues.pkl")
    return


buildModelForTokens()
buildModelForSentences()
'''
plt.subplot(2,1,1); plt.plot(F[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR');
plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy');
plt.subplot(2,1,1); plt.plot(F2[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR');
plt.subplot(2,1,2); plt.plot(F2[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy');
plt.subplot(2,1,1); plt.plot(F1[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR1');
plt.subplot(2,2,2); plt.plot(F[8,:]); plt.xlabel('Frame no'); plt.ylabel('spectral rolloff');
plt.subplot(2,2,2); plt.plot(F1[8,:]); plt.xlabel('Frame no'); plt.ylabel('spectral rolloff');
plt.subplot(2,2,2); plt.plot(F2[8,:]); plt.xlabel('Frame no'); plt.ylabel('spectral rolloff');
plt.subplot(2,1,2); plt.plot(F1[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy1'); plt.show()

'''






