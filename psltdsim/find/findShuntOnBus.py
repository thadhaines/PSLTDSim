def findShuntOnBus(mirror, Busnum, Id=None):
    """Find first load on bus unless Id specified
    Note that Ids are typically a strings i.e. '2' 
    """
    tic = time.time()
    # handle searching before search dictionary created.
    if not mirror.searchDict:
        for x in range(len(mirror.Shunt)):
            if mirror.Shunt[x].Busnum == Busnum:
                # Return first Shunt on bus if no Id
                if Id == None:
                    mirror.FindTime += time.time() - tic
                    return mirror.Shunt[x]

                if Id == mirror.Shunt[x].Id:
                    mirror.FindTime += time.time() - tic
                    return mirror.Shunt[x]
    else:
        # Handle searching after search dictionary is made
        bnum = str(int(Busnum))
        if bnum in mirror.searchDict:
            # bus found
            if 'Shunt' in mirror.searchDict[bnum]:
                # bus has Shunt
                if Id == None:
                    # return first Shunt if No id
                    mirror.FindTime += time.time() - tic
                    return mirror.searchDict[bnum]['Shunt'][0]

                else:
                    # find Shunt with matching ID
                    for bShunt in mirror.searchDict[bnum]['Shunt']:
                        if Id == bShunt.Id:
                            mirror.FindTime += time.time() - tic
                            return bShunt
    if Id:
        print("Shunt on Bus %s with Id %s not Found" % (bnum,Id))
    else:
        print("Shunt on Bus %d not Found" % Busnum)
    mirror.FindTime += time.time() - tic
    return None