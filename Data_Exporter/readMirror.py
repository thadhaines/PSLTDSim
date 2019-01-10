def readMirror(fileLocation):
    """Returns saved Model (mirror) from Pickled file at 'fileLocation'
    Note that:
        Imports must match those in LTD_sim 
        Values returned from PSLF objects must be cast to python types
        ( PSLF often returns single or int 16 -> cast as float or int )
    """
    import os
    import sys
    import pickle as pickle

    # path handling for tests
    # not needed in function...
    #print(os.getcwd())
    #os.chdir(r"C:\Users\thad\source\repos\thadhaines\LTD_sim\Data_Exporter")
    #sys.path.append(r"C:\Users\thad\source\repos\thadhaines\LTD_sim")
    #print(os.getcwd())

    from CoreAgents import AreaAgent, BusAgent, GeneratorAgent, SlackAgent, LoadAgent
    from Model import Model

    # when 'functionized', this is where the file location goes
    f = open(fileLocation,"rb")

    mir = pickle.load(f)
    f.close()
    print("Model Loaded!")
    print(mir)
    return mir