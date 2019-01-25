"""Functions to return object reference from mirror (model)"""

def findGenOnBus(mirror, Busnum, Id=None):
    """Find first generator on bus unless Id specified
    Note that Ids are typically a strings i.e. '2' 
    """

    for x in range(len(mirror.Machines)):
        if mirror.Machines[x].Busnum == Busnum:
            # Return first gen on bus if no Id
            if Id == None:
                return mirror.Machines[x]

            if Id == mirror.Machines[x].Id:
                return mirror.Machines[x]
    if Id:
        print("Generator on Bus %d with Id '%s'not Found" % (Busnum,Id))
    else:
        print("Generator on Bus %d not Found" % Busnum)
    return None

def findLoadOnBus(mirror, Busnum, Id=None):
    """Find first load on bus unless Id specified
    Note that Ids are typically a strings i.e. '2' 
    """

    for x in range(len(mirror.Load)):
        if mirror.Load[x].Bus.Extnum == Busnum:
            # Return first load on bus if no Id
            if Id == None:
                return mirror.Load[x]

            if Id == mirror.Load[x].Id:
                return mirror.Load[x]
    if Id:
        print("Load on Bus %d with Id '%s'not Found" % (Busnum,Id))
    else:
        print("Load on Bus %d not Found" % Busnum)
    return None