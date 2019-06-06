def findBranchByScanBusCk(mirror, ScanBus, Ck):
    """Return mirror bus object if possible"""
    tic = time.time()

    # required to use find functions during mirror creation before searchDict made
    if not mirror.branchDict:
        for branch in mirror.Branch:
            if branch.ScanBus == ScanBus:
                if bus.Ck == Ck:
                    mirror.FindTime += time.time() - tic
                    return branch
    else:
        indexNum = str(int(ScanBus))
        if indexNum in mirror.branchDict:
            if Ck in mirror.branchDict[indexNum]:
                mirror.FindTime += time.time() - tic
                return mirror.branchDict[indexNum][Ck]

    print("Branch with Index %d and Ck %s not found." % (Busnum, Ck))
    mirror.FindTime += time.time() - tic
    
    return None
