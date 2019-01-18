def saveMirror(mir, savName):
    """Creates pickle object of mirror named savName.pkl
    """
    import pickle as pickle

    savName = savName + '.pkl'    
    f = open(savName, "wb")
    print("Pickling Mirror object...")
    pickle.dump(mir, f) #  for highest, produces binary (other protocols may be faster)
    f.close
    print("Mirror object pickled to binary as '%s'" % savName)

    return   