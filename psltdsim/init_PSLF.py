def init_PSLF(locations, loadDyd = True):
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

    # truly global variables
    __builtin__.mid = mid
    __builtin__.col = col

    print('*** init_PSLF')

    # create pslf instance / object 
    __builtin__.PSLF = mid.Pslf(locations['pslfPath'])
    # load .sav file
    load_test = __builtin__.PSLF.LoadCase(locations['savPath'])

    if load_test == 0:
        print("*** " + locations['savPath'] + " Successfully loaded.")

        # Stop loading of dyd...
        #loadDyd = False

        # load dynamics into pslf
        if loadDyd:
            for dyd in locations['dydPath']:
                dyd_test = __builtin__.PSLF.LoadDynamics(dyd)

                if dyd_test == 0:
                    print("*** " + dyd + " Successfully loaded.")
                else:
                    print("Failure to load .dyd")
                    print("Error code: %d" % dyd_test)
                    raise SystemExit(0)
    else:
        print("Failure to load .sav")
        print("Error code: %d" % load_test)
        raise SystemExit(0)
    