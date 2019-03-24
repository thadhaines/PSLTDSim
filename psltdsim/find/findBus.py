def findBus(mirror, Busnum):
    """Return mirror bus object if possible"""
    for bus in mirror.Bus:
        if bus.Extnum == Busnum:
            return bus

    print("Bus %d not found." % Busnum)
    return None
