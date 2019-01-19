def loadModelDictionary(fileLocation):
    """Returns saved Model Dictionary from Pickled file at 'fileLocation'"""
    import os
    import sys
    import pickle as pickle

    print('inside Load Model Dict..')
    print(fileLocation)
    print(sys.version)
    print(os.getcwd())
    f = open(fileLocation,"rb")
    mir = pickle.load(f)
    f.close()
    print("Model Dictionary Loaded.")

    return mir