def loadModelDictionary(fileLocation):
    """Returns saved Model Dictionary from Pickled file at 'fileLocation'"""
    import os
    import sys
    import pickle as pickle

    # path handling for tests
    # should not needed in function as paths should be handled in main prog
    #print(os.getcwd())
    #os.chdir(r"C:\Users\thad\source\repos\thadhaines\LTD_sim\Data_Exporter")
    #sys.path.append(r"C:\Users\thad\source\repos\thadhaines\LTD_sim")
    #print(os.getcwd())

    #f = open(fileLocation,"rb")
    '''
    content = ''
    outsize = 0
    with open(fileLocation, 'rb') as infile:
        content = infile.read()
    with open(fileLocation, 'wb') as output:
        for line in content.splitlines():
            outsize += len(line) + 1
            output.write(line + str.encode('\n'))
    '''

    f = open(fileLocation,"rb")
    mir = pickle.load(f)
    f.close()
    print("Model Dictionary Loaded.")

    return mir