#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tracktime.py

Purpose:
    Provide info on time routines take

Version:
    1       First start, based on tracktime.ox

Date:
    2017/9/14

@author: cbs310
"""
###########################################################
### Imports
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import scipy.optimize as opt
# import seaborn as sns
# import statsmodels.api as sm
import time

###########################################################
### TrackInit()
def TrackInit():
    """
    Purpose:
      Initialise settings for timing routines through TrackTime()
    """
    global g_TT_names, g_TT_duration, g_TT_t0, g_TT_iR

    # print ("In TrackInit")
    g_TT_names= []
    g_TT_duration= []
    g_TT_t0= time.time()
    g_TT_iR= -1

###########################################################
### _TrackIndex()
def _TrackIndex(sR):
    global g_TT_names, g_TT_duration

    # In case sR= -1, just stop tracking time
    if (sR == -1):
        return -1

    if (not (sR in g_TT_names)):
        g_TT_names.append(sR)
        g_TT_duration.append(0.0)
    # else:
    #     print ("Found ", sR, " at index ", g_TT_names.index(sR))

    return g_TT_names.index(sR)

###########################################################
### TrackTime(sR)
def TrackTime(sR):
    """
    Purpose:
        Track the time routine sR takes
    """
    global g_TT_names, g_TT_duration, g_TT_t0, g_TT_iR

    if (not 'g_TT_names' in globals()):
        TrackInit()

    if (g_TT_iR >= 0):
        g_TT_duration[g_TT_iR]+= time.time() - g_TT_t0

    g_TT_iR= _TrackIndex(sR)
    g_TT_t0= time.time()

###########################################################
### TrackReport()
def TrackReport():
    """
    Purpose:
        Report the time routines took
    """
    global g_TT_names, g_TT_duration, g_TT_t0, g_TT_iR

    if (not 'g_TT_names' in globals()):
        TrackInit()

    if (g_TT_iR >= 0):
        g_TT_duration[g_TT_iR]+= time.time() - g_TT_t0

    vDur= np.array(g_TT_duration)
    dTot= np.sum(vDur)

    iRR= len(vDur)
    print ("Tijd doorgebracht per routine:")
    print ("%15s  %10s %8s" % ("Routine", "Secs", "Perc."))
    for i in range(iRR):
        print ("%15s: %10.2f %8.2f" % (g_TT_names[i], vDur[i], 100*vDur[i]/dTot))
    print ("Total: %10.2fs" % dTot)


###########################################################
def tic():
    #Homemade version of matlab tic and toc functions
    # import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()
###########################################################
def toc():
    # import time
    if 'startTime_for_tictoc' in globals():
        print ("Elapsed time: " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print ("Toc: start time not set")

###########################################################
### mY= lengthycalculation(iN, iS)
def lengthycalculation(iN, iS):
    mY= 0.0
    for j in range(iN):
        mX= np.random.randn(iS, iS)
        mY+= np.exp(mX)

    return mY

###########################################################
### main
def main():
    # Magic numbers
    iN= 100
    iSa= 5
    iSb= 10

    # estimation
    for i in range(iN):
        TrackTime("Routine A")
        mX= lengthycalculation(iN, iSa)

        TrackTime("Routine B")
        mX= lengthycalculation(iN, iSb)

        TrackTime(-1)

    # Output
    TrackReport()
    print ("This is a test\n")

###########################################################
### start main
if __name__ == "__main__":
    main()
