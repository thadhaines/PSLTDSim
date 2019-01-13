def makeModelDictionary(mir):
    """Makes dictionary of available Model data"""
    # TODO: make less nested, may enable easier MATLAB import...

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

            loadD = {}
            genD = {}
            slackD = {}

            # create dictionary of dictionaries for objects on bus
            for c_load in range(len(mir.Area[c_area].Bus[c_bus].Load)):
                loadD[c_load] = mir.Area[c_area].Bus[c_bus].Load[c_load].getDataDict()

            for c_gen in range(len(mir.Area[c_area].Bus[c_bus].Gens)):
                genD[c_gen] = mir.Area[c_area].Bus[c_bus].Gens[c_gen].getDataDict()

            for c_slk in range(len(mir.Area[c_area].Bus[c_bus].Slack)):
                slackD[c_slk] = mir.Area[c_area].Bus[c_bus].Slack[c_slk].getDataDict()

            # combine dictionaries to lone bus dictionary
            busD['load'] = loadD
            busD['gens'] = genD
            busD['slack'] = slackD

            # generate unique name for lone bus dit
            strBusName = str(mir.Area[c_area].Bus[c_bus].Extnum) # .zfill(3) if padding is desired

            # add lone bus to area bus dictionary
            areaBusD[strBusName] = busD

        # combine collected bus ditionary into area dictionary
        areaD['bus'] = areaBusD

        # generate unique name for area dictionary
        strAreaName = str(mir.Area[c_area].Area) # .zfill(3)
        # combine area dictionary into root area dictionary
        rootAreaD[strAreaName] = areaD

    # combine all areas to root D
    rootD['area'] = rootAreaD

    return rootD          