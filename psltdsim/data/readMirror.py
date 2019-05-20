def readMirror(fileLocation):
    """Returns saved Model (mirror) from Pickled file at 'fileLocation'
        Needed to transfer model from IPY to PY3
    """

    import pickle as pickle

    #f = open(fileLocation,"rb")
    import shelve
    import contextlib
    with contextlib.closing(shelve.open(fileLocation, 'r')) as shelf:
        mir = shelf['mir']
    #shelf['mir'] = mir
    
    #mir = pickle.load(f)
    #f.close()
    print("*** Mirror read from %s" % fileLocation.split('\\')[-1])

    return mir