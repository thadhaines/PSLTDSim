def readMirror(fileLocation):
    """Returns saved Model (mirror) from Pickled file at 'fileLocation'
        Needed to transfer model from IPY to PY3
    """

    import pickle as pickle

    f = open(fileLocation,"rb")

    mir = pickle.load(f)
    f.close()
    print("*** Mirror Loaded:")
    print(mir)

    return mir