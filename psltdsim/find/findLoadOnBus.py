def findLoadOnBus(mirror, Busnum, Id=None):
    """Find first load on bus unless Id specified
    Note that Ids are typically a strings i.e. '2' 
    """
    tic = time.time()
    if not mirror.searchDict:
        for x in range(len(mirror.Load)):
            if mirror.Load[x].Busnum == Busnum:
                # Return first gen on bus if no Id
                if Id == None:
                    mirror.FindTime += time.time() - tic
                    return mirror.Load[x]

                if Id == mirror.Load[x].Id:
                    mirror.FindTime += time.time() - tic
                    return mirror.Load[x]
    else:
        bnum = str(int(Busnum))
        if bnum in mirror.searchDict:
            # bus found
            if 'Load' in mirror.searchDict[bnum]:
                # bus has Load
                if Id == None:
                    # return first Load if No id
                    mirror.FindTime += time.time() - tic
                    return mirror.searchDict[bnum]['Load'][0]

                else:
                    # find Load with matching ID
                    for bLoad in mirror.searchDict[bnum]['Load']:
                        if Id == bLoad.Id:
                            mirror.FindTime += time.time() - tic
                            return bLoad
    if Id:
        print("Load on Bus %d with Id '%s' not Found" % (Busnum,Id))
    else:
        print("Load on Bus %d not Found" % Busnum)
    mirror.FindTime += time.time() - tic
    return None