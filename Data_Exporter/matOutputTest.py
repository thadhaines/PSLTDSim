"""Script will attempt to take pickled object and output data in a mat file"""
#NOTE: Python 3.6+ script

# for required linking of model files
import sys
import os
import scipy.io as sio

print(os.getcwd())
os.chdir(r"C:\Users\thad\source\repos\thadhaines\LTD_sim\Data_Exporter")
print(os.getcwd())
sys.path.append(r"C:\Users\thad\source\repos\thadhaines\LTD_sim")
from readMirror import readMirror

mir = readMirror('exportTest01.pkl')

# data for dictionary
a = [867,5309]
b = 'junkbond'
c = [1,2,3,4]

# dictionary
d = {'num':a,
     'trader': b}

# appending of data to dictionary [key] = value
d['test'] = c
d['newVar'] = mir.Bus[1].r_Vm
# becomes a MATLAB structure
d['dict'] = {"data" : [12,23,4,5], "data2":['more', 'data','yet','again'],'yeah':[584.8546]}

# Simiarl name could be generated iteratively while stepping through model.
dataName = "bus3_Vm" 

# writing .mat files
sio.savemat('nameOfMat.mat', {dataName:mir.Bus[3].r_Vm})
sio.savemat('yurp',d)

"""
Results:
    Runs in interactive mode - has an error when trying to run normally that
    results in: ModuleNotFoundError: No module named 'Image'

    sio.savemat only creates .mat files - it does not append to existing ones

    A way of working through model data and creating, then appending 
    unique dictionary keys and assocaited data to a single dictionary.
    This one dictionary will then be written to a .mat file.

    Additionally, this dictionary can contain other dictionaries that will
    'clean up' the data structure that will wind up in MATLAB. 
    'Could' mimic structure of python mirror as it may result in easier
    understanding of 'what's going on'
"""