def loadModelDictionary(fileLocation):
    """Returns saved Model Dictionary from Pickled file at 'fileLocation'"""
    import os
    import sys
    import pickle as pickle

    print('Loading %s...' % fileLocation)
    f= open(fileLocation,"rb")
    mir = pickle.load(f)

    f.flush()
    f.close()

    print("Model Dictionary Loaded!")

    return mir