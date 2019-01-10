"""Opens saved Model (mirror) Pickle
Results:
    Seems to work...
    Imports must match those in LTD_sim 
    Values returned from PSLF objects must be cast to python types
    i.e. PSLF often returns single or int 16 -> cast as float or int
"""
import os
import sys

try:
    import cPickle as pickle
except ModuleNotFoundError:
    # python 3 doesn't use cPickle
    import pickle as pickle

# path handling for tests
print(os.getcwd())
os.chdir(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim\Data_Exporter")
sys.path.append(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim")
print(os.getcwd())

from CoreAgents import AreaAgent, BusAgent, GeneratorAgent, SlackAgent, LoadAgent
from Model import Model

# when 'functionized', this is where the file location goes
f = open("exportTest02.pkl","rb")

mir = pickle.load(f)
f.close()
print("Model Loaded!")
print(mir)