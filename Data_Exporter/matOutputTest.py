"""Script will attempt to take pickled object and output data in a mat file"""
#NOTE: Uses >>32-bit<< Python 3.6+ script

import sys
import os
import scipy.io as sio
import numpy as np

from loadModelDictionary import loadModelDictionary

dictLoc = 'fullSysDict.pkl'
varName = 'mir1'

d = loadModelDictionary(dictLoc)

# For reference
#combinedD = {'VarName' : dict}
#sio.savemat('nameOfMat',combinedD)

mirD ={varName:d}
sio.savemat(varName, mirD)
print(varName +'.mat saved')

"""
Results:
    Runs!
    TODO: turn into a function, maybe rethink dictionary structure
"""