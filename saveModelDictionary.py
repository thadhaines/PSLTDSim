def saveModelDictionary(mirD, savName):
    """Creates pickle object of Model dictionary named savName.pkl
    Return savName
    """
    import os
    import pickle as pickle

    savName = savName + '.pkl'    
    f = open(savName, "wb")
    print("Pickling Dictionary object...")
    # create pickle,
    pickle.dump(mirD, f)

    # ensure file written to disk
    f.flush()
    os.fsync(f.fileno())
    f.close

    # for python 3.4+ importing
    # convert dos linefeeds (crlf) to unix (lf)
    # edited for explicit file closes

    content = ''
    outsize = 0
    infile= open(savName, 'rb')
    content = infile.read()
    infile.close()

    output =  open(savName, 'wb')
    for line in content.splitlines():
        outsize += len(line) + 1
        output.write(line + str.encode('\n'))

    # ensure file written to disk
    output.flush()
    os.fsync(output.fileno())
    output.close()

    print("Dictionary object pickled as '%s'" % savName)

    return savName