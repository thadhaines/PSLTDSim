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

            Nload = len(mir.Area[c_area].Bus[c_bus].Load)
            Ngen = len(mir.Area[c_area].Bus[c_bus].Gens)
            Nslack = len(mir.Area[c_area].Bus[c_bus].Slack)

            # create empty dictionaries if applicable
            if Nload>0:
                loadD = {}
            if Ngen>0:
                genD = {}
            if Nslack>0:
                slackD = {}

            # create dictionary of dictionaries for objects on bus
            for c_load in range(Nload):
                loadD[c_load] = mir.Area[c_area].Bus[c_bus].Load[c_load].getDataDict()

            for c_gen in range(Ngen):
                genD[c_gen] = mir.Area[c_area].Bus[c_bus].Gens[c_gen].getDataDict()

            for c_slk in range(Nslack):
                slackD[c_slk] = mir.Area[c_area].Bus[c_bus].Slack[c_slk].getDataDict()

            # combine dictionaries to lone bus dictionary, if they exist
            if Nload>0:
                busD['load'] = loadD
            if Ngen>0:
                busD['gens'] = genD
            if Nslack>0:
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
    #rootD['area'] = rootAreaD
    # removes Area from dictionary
    rootD['bus'] = rootAreaD
    return rootD          