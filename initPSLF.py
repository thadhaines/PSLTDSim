"""File to handle import of PSLF libraries
   and Creation of global PSLF object
   Replaces imports at begining of Model and init_PSLF function inside Model

   TODO: before implementation, all Model.pslf references must be corrected.
"""
import __builtin__

#ensure locations list exits
from __main__ import *

# load .NET dll
import clr # Common Language Runtime
clr.AddReferenceToFileAndPath(locations[0])
import GE.Pslf.Middleware as mid
import GE.Pslf.Middleware.Collections as col 

__builtin__.mid = mid
__builtin__.col = col

# create pslf instance / object
global PSFL 
__builtin__.PSLF = mid.Pslf(locations[1])   
# load .sav file
load_test = __builtin__.PSLF.LoadCase(locations[2])     

if load_test == 0:
    print(locations[2] + " Successfully loaded.")
else:
    print("Failure to load .sav")
    print("Error code: %d" % load_test)
    raise SystemExit(0)
    