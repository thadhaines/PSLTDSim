"""Script will attempt to take pickled object and output data in a mat file
NOTE: Obsolete? 05/26/19 """
#NOTE: Uses >>32-bit<< Python 3.6+ script

import sys
import os

#from .loadModelDictionary import loadModelDictionary

def makeMat(dictLoc, varName, fileDirectory):
    """Create varName.mat file from system dictionary
    Meant to be run from command....
    if fileDirectory is None, will look in current folder for file
    """
    import scipy.io as sio
    import numpy as np

    print(sys.version)
    if fileDirectory:
        cwd = os.getcwd()
        os.chdir(cwd + fileDirectory)

    print('*** Creating %s.mat...' % (varName))
    d = loadModelDictionary(dictLoc)

    # For reference
    #combinedD = {'VarName' : dict}
    #sio.savemat('nameOfMat',combinedD)

    mirD ={varName:d}
    sio.savemat(varName, mirD)
    print(varName +'.mat saved!')

    # remove pickled dictionary #NOTE: obsolete? 05/26/19
    delDict = None
    if delDict:
        os.remove(dictLoc)
        print('%s Deleted.')

    return

if __name__ == "__main__":
    dictLoc = sys.argv[1]
    varName = sys.argv[2]
    fileDirectory = sys.argv[3]
    makeMat(dictLoc, varName, fileDirectory)

"""
Results:
    Runs!
    TODO: maybe rethink dictionary structure
"""