def saveMirror(mir, savName):
    """Creates pickle object of mirror named savName.pkl
    """
    import pickle as pickle

    savName = savName + '.pkl'    
    f = open(savName, "wb")
    pickle.dump(mir, f,protocol=-1) #  for highest, produces binary
    f.close
    print("Mirror object pickled to binary as '%s'" % savName)

    return   