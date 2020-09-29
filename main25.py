# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:22:20 2020

@author: Martijn
"""

import numpy as np
import pandas as pd
import numpy.random as rnd
import scipy.stats as stats
from numpy.linalg import inv
from tracktime import *

def readData(sRegressors, sObservables, sTimeDep, sTimeHet):
    dfX = pd.read_csv(sRegressors, header = None)
    dfY = pd.read_csv(sObservables, header = None)
    dfTimeDep = pd.read_csv(sTimeDep, header = None)
    dfTimeHet = pd.read_csv(sTimeHet, header = None)
    return np.array(dfX), np.array(dfY), np.array(dfTimeDep), np.array(dfTimeHet)

def calcBeta_OLS(mX, mY):
    return inv((mX.T @ mX)) @ mX.T @ mY

def calcTstat(mBeta_OLS, mX, mY, n, m):
    mEpsilon = mY - mX @ mBeta_OLS
    mSigma = np.zeros((n,n,m))
    mVar = np.zeros((3, 3, m))
    for i in range(0, n):
        mSigma[i,i] = mEpsilon[i]**2
    for i in range(0, m):
        mVar[:,:,i] = inv((mX.T @ mX)) @ mX.T @ mSigma[:,:,i] @ mX @ inv((mX.T @ mX))
    vTstat = mBeta_OLS[2] / np.sqrt(mVar[2,2])
    return vTstat    

def calcRejectionRegion(dAlpha, n, k):
    c = stats.t.ppf(dAlpha/2, n - k)
    return c

def main():
    # Magic numbers
    sRegressors = "Regressors.txt"
    sObservables = "Observables.txt"
    sTimeDep = "Timeseries_dep.txt"
    sTimeHet = "Timeseries_het.txt"
 
    iSeed = 1234
    dAlpha = 0.05                    #significance level
    iB = 99                      #Number of simulations
    
    TrackTime("Read data")
    mX, mY, mTimeDep, mTimeHet = readData(sRegressors, sObservables, sTimeDep, sTimeHet)
    n, m = mY.shape
    k = len(mX[0])
    print(k)
    
    mBeta_OLS = calcBeta_OLS(mX, mY) 
    
    vTstat = calcTstat(mBeta_OLS, mX, mY, n, m)    
    c = calcRejectionRegion(dAlpha, n, k)
    print(np.logical_or(vTstat <= c, vTstat >= -c).sum())    
    
    TrackReport()
if __name__ == '__main__':
    main()