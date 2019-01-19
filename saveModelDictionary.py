def saveModelDictionary(mirD, savName):
    """Creates pickle object of Model dictionary named savName.pkl
    """
    import pickle as pickle

    savName = savName + '.pkl'    
    f = open(savName, "wb")
    print("Pickling Dictionary object...")
    pickle.dump(mirD, f)
    f.close

    # for python 3.4+ importing
    # convert dos linefeeds (crlf) to unix (lf)
    content = ''
    outsize = 0
    with open(savName, 'rb') as infile:
        content = infile.read()
    with open(savName, 'wb') as output:
        for line in content.splitlines():
            outsize += len(line) + 1
            output.write(line + str.encode('\n'))

    print("Dictionary object pickled to binary as '%s'" % savName)

    return   