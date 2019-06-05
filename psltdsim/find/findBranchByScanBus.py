def findBranchByScanBus(mirror, ScanBus):
    """Return mirror bus object if possible"""
    tic = time.time()

    # required to use find functions during mirror creation before searchDict made
    if not mirror.branchDict:
        for branch in mirror.Branch:
            if bus.ScanBus == ScanBus:
                mirror.FindTime += time.time() - tic
                return branch
    else:
        indexNum = str(int(ScanBus))
        if indexNum in mirror.branchDict:
            mirror.FindTime += time.time() - tic
            return mirror.branchDict[indexNum]

    print("Branch with Index %d not found." % Busnum)
    mirror.FindTime += time.time() - tic
    
    return None
