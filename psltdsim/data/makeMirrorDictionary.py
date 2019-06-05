def makeMirrorDictionary(mir):
    """Makes dictionary of various Mirror data"""
    # TODO: adjust as required to validate in MATLAB...
    import psltdsim as ltd

    rootD = mir.getDataDict()

    rootAreaD = {}

    areaN = []
    for c_area in range(len(mir.Area)):
        # for each area...
        areaD = mir.Area[c_area].getDataDict()

        # lists for bus indexs
        genBusN = []
        loadBusN = []
        slackBusN =[]
        shuntBusN = []
        xBusN = []

        # create empty dictionary to fill
        areaBusD = {}
        for c_bus in range(len(mir.Area[c_area].Bus)):
            # for each bus in c_area
            busD = mir.Area[c_area].Bus[c_bus].getDataDict()

            Nload = len(mir.Area[c_area].Bus[c_bus].Load)
            Ngen = len(mir.Area[c_area].Bus[c_bus].Gens)
            Nslack = len(mir.Area[c_area].Bus[c_bus].Slack)
            Nshunt = len(mir.Area[c_area].Bus[c_bus].Shunt)

            # create empty dictionaries if applicable and create bus ident
            ident = 'x'

            if Nshunt>0:
                shuntD = {}
                ident = 'H'
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
                loadD['L'+ str(c_load+1)] = mir.Area[c_area].Bus[c_bus].Load[c_load].getDataDict()
                loadBusN.append(  mir.Area[c_area].Bus[c_bus].Extnum ) # str(mir.Area[c_area].Bus[c_bus].Extnum).zfill(3) )

            for c_gen in range(Ngen):
                genD['G'+str(c_gen+1)] = mir.Area[c_area].Bus[c_bus].Gens[c_gen].getDataDict()
                genBusN.append(  mir.Area[c_area].Bus[c_bus].Extnum ) # str(mir.Area[c_area].Bus[c_bus].Extnum).zfill(3) )

            for c_slk in range(Nslack):
                slackD['S'+str(c_slk+1)] = mir.Area[c_area].Bus[c_bus].Slack[c_slk].getDataDict()
                slackBusN.append( mir.Area[c_area].Bus[c_bus].Extnum ) # str(mir.Area[c_area].Bus[c_bus].Extnum).zfill(3) )

            for c_shnt in range(Nshunt):
                shuntD['H'+str(c_shnt+1)] = mir.Area[c_area].Bus[c_bus].Shunt[c_shnt].getDataDict()
                shuntBusN.append( mir.Area[c_area].Bus[c_bus].Extnum )

            # combine dictionaries to lone bus dictionary, if they exist
            if Nload>0:
                busD = ltd.data.mergeDicts(busD, loadD)
            if Ngen>0:
                busD = ltd.data.mergeDicts(busD, genD)
            if Nslack>0:
                busD = ltd.data.mergeDicts(busD, slackD)
            if Nshunt>0:
                busD = ltd.data.mergeDicts(busD, shuntD)

            busD['Nload'] = Nload
            busD['Ngen'] = Ngen
            busD['Nslack'] = Nslack
            busD['Nshunt'] = Nshunt

            # generate unique name for lone bus dict
            strBusName = ident + str(mir.Area[c_area].Bus[c_bus].Extnum)#.zfill(3) #if padding is desired

            # add x bus to list of x busses
            if ident == 'x':
                xBusN.append(  mir.Area[c_area].Bus[c_bus].Extnum )

            # add lone bus to area bus dictionary
            areaBusD[strBusName] = busD

        # combine collected bus ditionary into area dictionary
        areaD = ltd.data.mergeDicts(areaD, areaBusD)
        areaD['genBusN'] = genBusN
        areaD['loadBusN'] = loadBusN
        areaD['slackBusN'] = slackBusN
        areaD['shuntBusN'] = shuntBusN
        areaD['xBusN'] = xBusN

        # generate unique name for area dictionary
        strAreaName = 'A' + str(mir.Area[c_area].Area) #.zfill(3)
        areaN.append(mir.Area[c_area].Area)

        # combine area dictionary into root area dictionary
        rootAreaD[strAreaName] = areaD

    # combine all areas to root D
    rootD = ltd.data.mergeDicts(rootD, rootAreaD)
    rootD['areaN'] = areaN

    return rootD          