#@patch('Model.Model', mir) # this may aid in changing object params before pickel
def saveMirror(mir, savName):
    """Creates pickle object of mirror named savName.pkl
    Idea is to send mirror data from ironpython to python 3 because
    Many more exporter options are available in python 3
    """

    #NOTE - this crashes if any PSLF data objects are saved inside the mirror
    # from __main__ import Model, BusAgent
    import pickle as p

    from Model import Model
    from CoreAgents import AreaAgent, BusAgent, GeneratorAgent, SlackAgent, LoadAgent

    Model.pslf = None
    mir.pslf = None
    # None of these attempts have changed what is written in pickle
    # Possibly because they're not written that way in the mirror?
    
    print(Model.__module__)
    #Model.__module__ = 'Model' # Alterations of module lead to Model.Model doesn't match Model.Model...
    print(BusAgent.__module__)
    savName = savName + '.pkl'    

    f = open(savName, "wb")
    #@patch('Model.Model', mir)
    p.dump(mir, f ) # protocol=-1 for highest, produces binary
    f.close
    print("Mirror object pickled to binary as '%s'" % savName)

    return   