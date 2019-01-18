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

    f = open(fileLocation,"rb")

    mir = pickle.load(f)
    f.close()
    print("Model Dictionary Loaded.")

    return mir