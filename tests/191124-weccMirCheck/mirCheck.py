""" File to scan mirror for unused machines and governors,
additionaly, check for models that may have a 0.0 as a droop """

import os
import psltdsim as ltd

#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")
#os.chdir(r"C:\Users\thad\source\repos\thadhaines\PSLTDSim")

dirname = os.path.dirname(__file__)

mirLoc = os.path.join(dirname, 'delme','genMW','genMWstepF.mir') # base case for AGC testing

mir = ltd.data.readMirror(mirLoc)
