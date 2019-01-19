"""Script will attempt to take pickled object and output data in a mat file"""
#NOTE: Uses >>32-bit<< Python 3.6+ script

import sys
import os
import scipy.io as sio
import numpy as np

from loadModelDictionary import loadModelDictionary

def makeMat(dictLoc, varName):
    """Create varName.mat file from system dictionary
    Meant to be run from command....
    """
    print(dictLoc)
    print(varName)
    print(sys.version)

    d = loadModelDictionary(dictLoc)

    # For reference
    #combinedD = {'VarName' : dict}
    #sio.savemat('nameOfMat',combinedD)

    mirD ={varName:d}
    sio.savemat(varName, mirD)
    print(varName +'.mat saved')

if __name__ == "__main__":
    dictLoc = sys.argv[1]
    varName = sys.argv[2]
    makeMat(dictLoc, varName)

"""
Results:
    Runs!
    TODO: maybe rethink dictionary structure
"""