def loadMirrorDictionary(fileLocation):
    """Returns saved Mirror Dictionary from Pickled file at 'fileLocation'"""
    import os
    import sys
    import pickle as pickle

    print('*** Loading %s...' % fileLocation)
    f= open(fileLocation,"rb")
    mir = pickle.load(f)

    f.flush()
    f.close()
    
    print("*** Mirror Dictionary Loaded!")

    return mir