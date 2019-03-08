"""File to handle import of PSLF libraries and Creation of global PSLF object

"""
import __builtin__

# load .NET dll
import clr # Common Language Runtime

def init_PSLF(locations):
	clr.AddReferenceToFileAndPath(locations['fullMiddlewareFilePath'])
	import GE.Pslf.Middleware as mid
	import GE.Pslf.Middleware.Collections as col 

	__builtin__.mid = mid
	__builtin__.col = col

	# create pslf instance / object 
	__builtin__.PSLF = mid.Pslf(locations['pslfPath'])   
	# load .sav file
	load_test = __builtin__.PSLF.LoadCase(locations['savPath'])     

	if load_test == 0:
	    print(locations['savPath'] + " Successfully loaded.")
	else:
	    print("Failure to load .sav")
	    print("Error code: %d" % load_test)
	    raise SystemExit(0)
    