def findGenOnBus(mirror, Busnum, Id=None, timing = True):
    """Find first generator on bus unless Id specified
    Note that Ids are typically a strings i.e. '2' 
    """
    # TODO: remove this import 
    import time

    if timing: tic = time.time()
    if mirror.debug:
        print('***Searching Bus %d for gen with ID %s...' %(Busnum, Id))
    if not mirror.searchDict:
        for x in range(len(mirror.Machines)):
            if mirror.Machines[x].Busnum == Busnum:
                # Return first gen on bus if no Id
                if mirror.debug:
                    print('***Found gen on Bus %d with ID %s...' %(mirror.Machines[x].Busnum, mirror.Machines[x].Id))
                if Id == None:
                    if timing: mirror.FindTime += time.time() - tic
                    return mirror.Machines[x]

                if Id == mirror.Machines[x].Id:
                    mirror.FindTime += time.time() - tic
                    return mirror.Machines[x]
    else:
        bnum = str(int(Busnum))
        if bnum in mirror.searchDict:
            # bus found
            if 'Machines' in mirror.searchDict[bnum]:
                # bus has machines
                if Id == None:
                    # return first gen if No id
                    if timing: mirror.FindTime += time.time() - tic
                    return mirror.searchDict[bnum]['Machines'][0]

                else:
                    # find gen with matching ID
                    for bGen in mirror.searchDict[bnum]['Machines']:
                        if bGen.Id == Id:
                            if timing: mirror.FindTime += time.time() - tic
                            return bGen
    if Id:
        print("Generator on Bus %d with Id '%s' not Found" % (Busnum,Id))
    else:
        print("Generator on Bus %d not Found" % Busnum)
    if timing: mirror.FindTime += time.time() - tic
    return None
