def findGenOnBus(mirror, Busnum, Id=None):
    """Find first generator on bus unless Id specified
    Note that Ids are typically a strings i.e. '2' 
    """
    tic = time.time()
    for x in range(len(mirror.Machines)):
        if mirror.Machines[x].Busnum == Busnum:
            # Return first gen on bus if no Id
            if Id == None:
                mirror.FindTime += time.time() - tic
                return mirror.Machines[x]

            if Id == mirror.Machines[x].Id:
                mirror.FindTime += time.time() - tic
                return mirror.Machines[x]
    if Id:
        print("Generator on Bus %d with Id '%s'not Found" % (Busnum,Id))
    else:
        print("Generator on Bus %d not Found" % Busnum)
    mirror.FindTime += time.time() - tic
    return None
