def findBus(mirror, Busnum):
    """Return mirror bus object if possible"""
    tic = time.time()
    for bus in mirror.Bus:
        if bus.Extnum == Busnum:
            mirror.FindTime += time.time() - tic
            return bus

    print("Bus %d not found." % Busnum)
    mirror.FindTime += time.time() - tic
    return None
