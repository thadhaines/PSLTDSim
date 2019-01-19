def makeModelDictionary(mir):
    """Makes dictionary of available Model data"""
    # TODO: make less nested, may enable easier MATLAB import...
    # TODO: append character to variable names that are only number 

    rootD = mir.getDataDict()

    rootAreaD = {}

    for c_area in range(len(mir.Area)):
        # for each area...
        areaD = mir.Area[c_area].getDataDict()

        # create empty dictionary to fill
        areaBusD = {}
        for c_bus in range(len(mir.Area[c_area].Bus)):
            # for each bus in c_area
            busD = mir.Area[c_area].Bus[c_bus].getDataDict()

            Nload = len(mir.Area[c_area].Bus[c_bus].Load)
            Ngen = len(mir.Area[c_area].Bus[c_bus].Gens)
            Nslack = len(mir.Area[c_area].Bus[c_bus].Slack)

            # create empty dictionaries if applicable and create bus ident
            ident = 'x'

            if Nload>0:
                loadD = {}
                ident = 'L'
            if Ngen>0:
                genD = {}
                ident = 'G'
            if Nslack>0:
                slackD = {}
                ident = 'S'

            # create dictionary of dictionaries for objects on bus
            for c_load in range(Nload):
                loadD['L'+ str(c_load)] = mir.Area[c_area].Bus[c_bus].Load[c_load].getDataDict()

            for c_gen in range(Ngen):
                genD['G'+str(c_gen)] = mir.Area[c_area].Bus[c_bus].Gens[c_gen].getDataDict()

            for c_slk in range(Nslack):
                slackD['S'+str(c_slk)] = mir.Area[c_area].Bus[c_bus].Slack[c_slk].getDataDict()

            # combine dictionaries to lone bus dictionary, if they exist
            if Nload>0:
                #busD['load'] = loadD
                busD = mergeDicts(busD, loadD)
            if Ngen>0:
                busD = mergeDicts(busD, genD)
            if Nslack>0:
                busD = mergeDicts(busD, slackD)

            # generate unique name for lone bus dit
            strBusName = ident + str(mir.Area[c_area].Bus[c_bus].Extnum) #.zfill(3) #if padding is desired

            # add lone bus to area bus dictionary
            areaBusD[strBusName] = busD
            #areaBusD = mergeDicts(busD)

        # combine collected bus ditionary into area dictionary
        areaD = mergeDicts(areaD, areaBusD)

        # generate unique name for area dictionary
        strAreaName = 'A' + str(mir.Area[c_area].Area) #.zfill(3)
        # combine area dictionary into root area dictionary
        mergeDicts()
        rootAreaD[strAreaName] = areaD

    # combine all areas to root D
    rootD = mergeDicts(rootD, rootAreaD)

    return rootD          