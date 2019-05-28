def findGenOnBus(mirror, Busnum, Id=None):
    """Find first generator on bus unless Id specified
    Note that Ids are typically a strings i.e. '2' 
    """
    tic = time.time()
    if not mirror.searchDict:
        for x in range(len(mirror.Machines)):
            if mirror.Machines[x].Busnum == Busnum:
                # Return first gen on bus if no Id
                if Id == None:
                    mirror.FindTime += time.time() - tic
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
                    mirror.FindTime += time.time() - tic
                    return mirror.searchDict[bnum]['Machines'][0]

                else:
                    # find gen with matching ID
                    for bGen in mirror.searchDict[bnum]['Machines']:
                        if bGen.Id == Id:
                            mirror.FindTime += time.time() - tic
                            return bGen
    if Id:
        print("Generator on Bus %d with Id '%s' not Found" % (Busnum,Id))
    else:
        print("Generator on Bus %d not Found" % Busnum)
    mirror.FindTime += time.time() - tic
    return None
