def saveModelDictionary(mirD, savName):
    """Creates pickle object of Model dictionary named savName.pkl
    """
    import pickle as pickle

    savName = savName + '.pkl'    
    f = open(savName, "wb")
    print("Pickling Dictionary object...")
    pickle.dump(mirD, f) #  for highest, produces binary (other protocols may be faster)
    f.close
    print("Dictionary object pickled to binary as '%s'" % savName)

    return   