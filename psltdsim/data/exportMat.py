"""Script will attempt to take pickled object and output data in a mat file
NOTE: will probably change when using py3 as data 'historian' """
#NOTE: Uses >>32-bit<< Python 3.6+ script

import sys
import os

def exportMat(mirror, simParams):
    """Create simParams['fileDirectory']\simParams['fileName'].mat  from mirror
    """
    import psltdsim as  ltd
    import scipy.io as sio
    import numpy as np

    d = ltd.data.makeMirrorDictionary(mirror)
    varName = simParams['fileName']

    if simParams['fileDirectory']:
        cwd = os.getcwd()
        os.chdir(cwd + simParams['fileDirectory'])

    print('Creating %s.mat from %s...' % (varName, simParams['fileDirectory']))

    mirD ={varName:d}
    sio.savemat(varName, mirD)
    print(varName +'.mat saved!')

    os.chdir(cwd)
    return