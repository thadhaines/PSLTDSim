def init_PSLF(locations):
    """Import PSLF libraries and Creation of global PSLF object
    IPY specific imports done inside function so MIRROR can be 
    used in PY3 and IPY
    """

    import __builtin__
    # load .NET dll
    import clr # Common Language Runtime

    clr.AddReferenceToFileAndPath(locations['middlewareFilePath'])
    import GE.Pslf.Middleware as mid
    import GE.Pslf.Middleware.Collections as col 

    __builtin__.mid = mid
    __builtin__.col = col

    # create pslf instance / object 
    __builtin__.PSLF = mid.Pslf(locations['pslfPath'])
    # load .sav file
    load_test = __builtin__.PSLF.LoadCase(locations['savPath'])

    if load_test == 0:
        # load dynamics into pslf
        dyd_test = __builtin__.PSLF.LoadDynamics(locations['dydPath'][0])
        print("*** " + locations['savPath'] + " Successfully loaded.")
        print("*** Result of loading %s: %d" % (locations['dydPath'][0], dyd_test))
    else:
        print("Failure to load .sav")
        print("Error code: %d" % load_test)
        raise SystemExit(0)
    