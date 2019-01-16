"""Script will attempt to take pickled object and output data in a mat file"""
#NOTE: Uses >>32-bit<< Python 3.6+ script

import sys
import os
import scipy.io as sio
import numpy as np

# for required linking of model files
print(os.getcwd())
#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim\Data_Exporter")
os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\LTD_sim\Data_Exporter")
#print(os.getcwd())
#sys.path.append(r"C:\Users\thad\source\repos\thadhaines\LTD_sim")
sys.path.append(r"D:\Users\jhaines\source\Repos\thadhaines\LTD_sim")
sys.path.append(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim")

from readMirror import readMirror
from loadModelDictionary import loadModelDictionary

#mir = readMirror('exportTestMicroMirW.pkl')

#d = loadModelDictionary('fullSysDict.pkl')
gen = loadModelDictionary('gen.pkl')
bus = loadModelDictionary('bus.pkl')
sy1 = loadModelDictionary('sys.pkl')
load = loadModelDictionary('load.pkl')

# For reference
#combinedD = {'VarName' : dict}
#sio.savemat('nameOfMat',combinedD)

busCol = {'bus' : bus}
genCol = {'gen': gen}

#sio.savemat('system', d)
sio.savemat('gen', genCol)
sio.savemat('bus', busCol)
sio.savemat('sys', sy1)
sio.savemat('load', load)

"""
Results:
    Runs in interactive mode, though writing dictionary doesn't work in interactive
    May get: ModuleNotFoundError: No module named 'Image' - fixed by installing Image

    sio.savemat only creates .mat files - it does not append to existing ones

    Nested structures don't seem to be saved correctly
   
    steps:
        export model dictionary from ipy, import into 3.7, 
        export dictionary to matlab....

        number of nests may be causing an issue as individual 
        dictionaries can be exported correctly

        Variable name (all numbers) not allowed - must append character to be MATLAB complient
"""