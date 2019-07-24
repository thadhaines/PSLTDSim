def makeBusSearchDict(mirror):
    """ returns dictionary used in updated search"""
    finDict = {}
    namesDict = {}
    mFlag = False # creates machines entry
    for bus in mirror.Bus:

        # index bus by external number
        finDict[str(bus.Extnum)] = {'Bus':bus}
        # populate rest of bus dictionary with agents
        if len(bus.Slack) > 0:
            finDict[str(bus.Extnum)]['Slack'] = bus.Slack
            mFlag = True

        if len(bus.Gens) > 0:
            finDict[str(bus.Extnum)]['Gens'] = bus.Gens
            mFlag = True

        if mFlag:
            finDict[str(bus.Extnum)]['Machines'] = bus.Slack + bus.Gens
            mFlag = False

        if len(bus.Load) > 0:
            finDict[str(bus.Extnum)]['Load'] = bus.Load

        if len(bus.Shunt) > 0:
            finDict[str(bus.Extnum)]['Shunt'] = bus.Shunt

        if len(bus.SVD) > 0:
                finDict[str(bus.Extnum)]['SVD'] = bus.SVD

        namesDict[bus.Busnam] = bus.Extnum

    # Add names dictionary to final dictionary
    finDict['Names'] = namesDict
    return finDict