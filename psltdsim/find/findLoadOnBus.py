def findLoadOnBus(mirror, Busnum, Id=None):
    """Find first load on bus unless Id specified
    Note that Ids are typically a strings i.e. '2' 
    """
    tic = time.time()
    for x in range(len(mirror.Load)):
        if mirror.Load[x].Bus.Extnum == Busnum:
            # Return first load on bus if no Id
            if Id == None:
                mirror.FindTime += time.time() - tic
                return mirror.Load[x]

            if Id == mirror.Load[x].Id:
                mirror.FindTime += time.time() - tic
                return mirror.Load[x]
    if Id:
        print("Load on Bus %d with Id '%s'not Found" % (Busnum,Id))
    else:
        print("Load on Bus %d not Found" % Busnum)
    mirror.FindTime += time.time() - tic
    return None