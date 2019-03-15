import pickle as pickle
import os

def saveMirror(mir, simParams):
    """Creates pickle object of mirror named savName.mir
    Returns full path to saved file
    """

    # Change current working directory to data destination.
    cwd = os.getcwd()
    savDir = cwd

    if simParams['fileDirectory'] :
        savDir = cwd + simParams['fileDirectory']
        os.chdir(savDir)

    savName = simParams['fileName']
    savName = savName + '.mir'    
    f = open(savName, "wb")
    print("*** Pickling Mirror object...")
    pickle.dump(mir, f)
    f.close

    fileLoc = savDir + savName
    print("*** Mirror object saved to binary: \n*** '%s'" 
          % (fileLoc))

    # Ensure return to initial working directory
    os.chdir(cwd)

    return fileLoc