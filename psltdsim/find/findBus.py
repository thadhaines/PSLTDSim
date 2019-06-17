def findBus(mirror, Busnum):
    """Return mirror bus object if possible"""
    tic = time.time()

    # required to use find functions during mirror creation before searchDict made
    if not mirror.searchDict:
        for bus in mirror.Bus:
            if bus.Extnum == Busnum:
                mirror.FindTime += time.time() - tic
                return bus
    else:
        bnum = str(int(Busnum))
        if bnum in mirror.searchDict:
            mirror.FindTime += time.time() - tic
            return mirror.searchDict[bnum]['Bus']

    print("Bus %s not found." % bnum)
    mirror.FindTime += time.time() - tic
    
    return None
