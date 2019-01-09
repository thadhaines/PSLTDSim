"""Testing Reading of pickled mirror
Results:
    Doesn't work without having definitions of objects
    Some object properties are defined as PSLF objects
    Python 3 doesn't use the clr library
    Options:
        Refactor LTD models to not involve PSLF objects

    Additionally, the pickle file has __main__ for objects module
    __module__ should be set to the file name that functions are 
    defined in.
"""
# work around for working directory
import os
import sys
print(os.getcwd())
os.chdir(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim\Data_Exporter")
sys.path.append(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim")
print(os.getcwd())

print(dir())

import cPickle as p
import Model 
from CoreAgents import *
from PerturbanceAgents import *

#del Model.__module__
#setattr(sys.modules[__name__], 'Model')

print(dir())
f = open("exportTest.pkl","rb")
mir = p.load(f)
f.close()