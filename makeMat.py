"""Script will attempt to take pickled object and output data in a mat file"""
#NOTE: Uses >>32-bit<< Python 3.6+ script

import sys
import os
import scipy.io as sio
import numpy as np

from loadModelDictionary import loadModelDictionary

def makeMat(dictLoc, varName, delDict):
    """Create varName.mat file from system dictionary
    Meant to be run from command....
    """
    print(sys.version)
    print('Creating %s.mat from %s...' % (varName, dictLoc))
    d = loadModelDictionary(dictLoc)

    # For reference
    #combinedD = {'VarName' : dict}
    #sio.savemat('nameOfMat',combinedD)

    mirD ={varName:d}
    sio.savemat(varName, mirD)
    print(varName +'.mat saved!')

    # remove pickled dictionary
    if delDict:
        os.remove(dictLoc)
        print('%s Deleted.')

if __name__ == "__main__":
    dictLoc = sys.argv[1]
    varName = sys.argv[2]
    delDict = int(sys.argv[3])
    makeMat(dictLoc, varName, delDict)

"""
Results:
    Runs!
    TODO: maybe rethink dictionary structure
"""