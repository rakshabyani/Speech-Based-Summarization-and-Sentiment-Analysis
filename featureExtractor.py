from pyAudioAnalysis import audioBasicIO, audioFeatureExtraction
import matplotlib.pyplot as plt
from matplotlib.mlab import find
from dataLocations import dataParameters
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
    f0=round(len(index) *Fs /(2*np.prod(len(signal))))
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
    values['F0'] = getPitch(x,Fs)
    values['loudness'] = getRMS(x)
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

def getDataFrame(filePath,emotion):
    '''
    @getDataFrame creates a model for each emotion in the fragment folder
    :param filePath: folder containing sound fragments for different emotions
    :param emotion: emotion name
    :return: model for the emotion as pandas Data Frame
    '''
    df = pd.DataFrame(columns=('F0', 'spectralCentroid', 'MFCC', 'energy', 'chroma', 'spectralFlux', 'spectralSpread', 'spectralEntropy', 'ZCR', 'loudness', 'energyEntropy', 'chromaDeviation', 'spectralRolloff'))
    path = filePath+emotion
    for filename in listFiles(path):
        try:
            val = getFeatures(path+"/"+filename)
            df.loc[filename.split(".")[0]] = val.values()
        except Exception as e:
            print filename, emotion, e.message
    return df

def buildModel():
    '''
    @buildModel builds the model for each emotion
    :return:
    '''
    path = dataParameters.getPath("wavTargets")
    modelPath = dataParameters.getPath("modelResults")
    for folder in listFiles(path):
        df = getDataFrame(path,folder)
        df.to_pickle(modelPath+folder+".pkl")
    return


#buildModel()

'''plt.subplot(2,1,1); plt.plot(F[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR');
plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy');
plt.subplot(2,1,1); plt.plot(F2[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR');
plt.subplot(2,1,2); plt.plot(F2[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy');
plt.subplot(2,1,1); plt.plot(F1[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR1');
plt.subplot(2,2,2); plt.plot(F[8,:]); plt.xlabel('Frame no'); plt.ylabel('spectral rolloff');
plt.subplot(2,2,2); plt.plot(F1[8,:]); plt.xlabel('Frame no'); plt.ylabel('spectral rolloff');
plt.subplot(2,2,2); plt.plot(F2[8,:]); plt.xlabel('Frame no'); plt.ylabel('spectral rolloff');
plt.subplot(2,1,2); plt.plot(F1[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy1'); plt.show()

'''






