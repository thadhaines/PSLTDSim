import pickle as pickle
import os

def saveMirror(mir, simParams):
    """Pickles Mirror to simParams['fileDirectory']\savName.mir
    Returns full path to saved file
    """

    # Change current working directory to data destination.
    cwd = os.getcwd()
    savDir = cwd

    if simParams['fileDirectory'] :
        # check if path doesn't exist - make if not
        path = cwd + simParams['fileDirectory']
        if not os.path.isdir(path):
            try:  
                os.mkdir(path)
            except OSError:  
                print ("Creation of the directory %s failed" % path)
            else:  
                print ("Successfully created the directory %s " % path)

        savDir = path
        os.chdir(savDir)


    savName = simParams['fileName']
    savName = savName + '.mir'    
    #f = open(savName, "wb")
    #print("*** Pickling Mirror object...")

    import contextlib
    import shelve
    #import dbm # not on windows
    #dbm._defaultmod = dbm.ndbm

    with contextlib.closing(shelve.open(savName, 'c')) as shelf:
        shelf['mir'] = mir
    #pickle.dump(mir, f)
    #f.close

    fileLoc = savDir + savName
    print("*** Mirror object saved to binary: \n*** '%s'" 
          % (fileLoc))

    # Ensure return to initial working directory
    os.chdir(cwd)

    return fileLoc