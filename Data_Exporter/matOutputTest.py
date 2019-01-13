"""Script will attempt to take pickled object and output data in a mat file"""
#NOTE: Uses >>32-bit<< Python 3.6+ script

import sys
import os
import scipy.io as sio
import numpy as np

# for required linking of model files
print(os.getcwd())
os.chdir(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim\Data_Exporter")
#print(os.getcwd())
#sys.path.append(r"C:\Users\thad\source\repos\thadhaines\LTD_sim")
#sys.path.append(r"D:\Users\jhaines\source\Repos\thadhaines\LTD_sim")
sys.path.append(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim")

from readMirror import readMirror
from loadModelDictionary import loadModelDictionary

mir = readMirror('exportTestMiniF5Mir.pkl')

# to test differenece between making a dictionary with numpy arrays.
dict1 = loadModelDictionary('exportTestMiniF5D.pkl')
# dict2 = makeModelDictionaryPY3(mir)

# For reference
#combinedD = {'VarName' : dict}
#sio.savemat('nameOfMat',combinedD)

unchanged = { 'unchagned' : dict1 }

sio.savemat('test1', unchanged)
sio.savemat('test2', dict1)

"""
Results:
    Runs in interactive mode - has an error when trying to run normally that
    results in: ModuleNotFoundError: No module named 'Image' - fixed by installing Image

    sio.savemat only creates .mat files - it does not append to existing ones

    Nested structures don't seem to be saved correctly
    Possibly using numpy arrays to solve problem...
    steps:
        export model from ipy, import into 3.7, create dictionay with np arrys,
        export dictionary to matlab....

        requires altering getDataDict in Model, CoreAgents...

        number of nests may be causing an issue....
"""