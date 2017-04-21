from sklearn.naive_bayes import GaussianNB,MultinomialNB
from dataLocations import dataParameters
from utils import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gnb = GaussianNB()
probabilityArray = []
predictedClassArray = []


def classify():
    path = dataParameters.getPath("modelResults")
    # path = path + "/models/"
    df= pd.DataFrame(columns=('F0', 'spectralCentroid', 'MFCC', 'energy', 'chroma', 'spectralFlux', 'spectralSpread', 'spectralEntropy', 'ZCR', 'loudness', 'energyEntropy', 'chromaDeviation', 'spectralRolloff'))
    for f in listFiles(path):
        if "pkl" in f.split(".")[1]:
        # if f == "averageValues.pkl":
            df1 = pd.read_pickle(path+f)
            df1.index=[f.split(".")[0]]*len(df1.index)
            df = pd.concat([df,df1])
    #print df

    for feature in df:
        df1 = df[feature]
        l = []
        if feature == 'F0':
            l = df1.tolist()
        elif feature == 'loudness':
            l = df1.tolist()
        elif feature == 'MFCC':
            for array in np.array(df1,dtype=pd.Series):
                l.append(array.flatten())
        elif feature == 'chroma':
            for array in np.array(df1,dtype=pd.Series):
                l.append(array.flatten())
        else:
            # fig = plt.figure(figsize=(10,10))
            # df1.plot(ax=fig.gca())
            # plt.scatter(df[feature],y=df.index.values)
            for array in np.array(df1,dtype=pd.Series):
                l.append(array[0])
            # plt.subplot(2, 1, 2)
            # plt.plot(l)
            # plt.xlabel('Frame no')
            # plt.ylabel('Spectral Centroid')
        gnb.fit(X=l, y=df1.index.values)
        prediction(feature)
    print probabilityArray
    print max(probabilityArray[0])


    '''
    # TESTING
    l=[]
    df1 = df['MFCC']
    for array in np.array(df1,dtype=pd.Series):
        l.append(array.flatten())
        # l.append(array[0].flatten())
        # l.append(array[0])
    gnb.fit(X=l, y=df1.index.values)
    '''

'''
prepareTestData.py calls predict method with dataframe as input. Dataframe contains :
Feature(index) and corresponding feature value
'''


def predict_emotion(df):
    feature = df.index
    df1 = df[feature]
    l = []
    if feature == 'F0':
        l = df1.tolist()
    elif feature == 'loudness':
        l = df1.tolist()
    elif feature == 'MFCC':
        for array in np.array(df1, dtype=pd.Series):
            l.append(array.flatten())
    elif feature == 'chroma':
        for array in np.array(df1, dtype=pd.Series):
            l.append(array.flatten())
    else:
        for array in np.array(df1, dtype=pd.Series):
            l.append(array[0])
    predicted_class = gnb.predict(l)
    predictedClassArray.append(predicted_class)


'''
For testing purpose
'''


def prediction(feature):
    l = [[2000.0]]
    if feature == 'F0':
        temp = gnb.predict(l)
        print "F0 result : "
        print temp
        # calculateProbability(temp)
        # probabilityArray.append(gnb.predict_log_proba([[2000.0]])[0,:])
    elif feature =="loudness" :
        temp = gnb.predict_log_proba([[4581.01473475]])[0,:]
        print "loudness result : "
        calculateProbability(temp)
        # print type(gnb.predict_log_proba([[4581.01473475]])[0,:])
    elif feature == 'spectralCentroid':
        print "spectralCentroid result : "
        temp = gnb.predict_log_proba([[0.18763865 , 0.18211618 , 0.15692214 , 0.12924414 , 0.09852054 , 0.07159376,
   0.05121942 , 0.03546902 , 0.02580975 , 0.01773863 , 0.0111586  , 0.00746279,
   0.00614419  ,0.00552024  ,0.00401932  ,0.00335678  ,0.00262406  ,0.00130429,
   0.00073348 , 0.00067195 , 0.00037249, 0.00035961, 0.         , 0.          , 0.,
   0.         , 0.         , 0.        , 0.        , 0.         , 0.          , 0.,
   0.         , 0.         , 0.        , 0.        , 0.         , 0.          , 0.,
   0.         , 0.         , 0.        , 0.        , 0.         , 0.          , 0.,
   0.         , 0.         , 0.        , 0.        , 0.         , 0.          , 0.,
   0.         , 0.         , 0.        , 0.        , 0.         , 0.          , 0.,
   0.         , 0.         , 0.        , 0.        , 0.]])[0,:]
        calculateProbability(temp)
    elif feature == 'energy':
        print "energy result : "
        temp = gnb.predict_proba([[1.27395856e-01, 1.88070018e-01, 1.98825873e-01, 1.64537552e-01 ,1.17334650e-01, 7.50584261e-02, 5.02411266e-02, 3.47230933e-02,2.06567827e-02, 1.11898236e-02, 6.36632787e-03, 3.31324778e-03,1.20605774e-03, 5.82086483e-04, 1.95212213e-04, 7.98220687e-05,2.90136531e-05, 7.05338740e-05, 9.07544835e-05, 3.31233450e-05,4.40792658e-07, 1.79266584e-07, 0.00000000e+00, 0.00000000e+00 ,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00 ,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00]])[0,:]
        calculateProbability(temp)
        print gnb.predict_proba([[1.27395856e-01, 1.88070018e-01, 1.98825873e-01, 1.64537552e-01 ,1.17334650e-01, 7.50584261e-02, 5.02411266e-02, 3.47230933e-02,2.06567827e-02, 1.11898236e-02, 6.36632787e-03, 3.31324778e-03,1.20605774e-03, 5.82086483e-04, 1.95212213e-04, 7.98220687e-05,2.90136531e-05, 7.05338740e-05, 9.07544835e-05, 3.31233450e-05,4.40792658e-07, 1.79266584e-07, 0.00000000e+00, 0.00000000e+00 ,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00 ,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00]])[0,:]

def calculateProbability(temp) :
    if probabilityArray.__len__() == 0:
        probabilityArray.append(temp)
    else:
        probabilityArray[0] += temp

classify()


