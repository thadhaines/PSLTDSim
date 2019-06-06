def makeBranchDict(mirror):
    """Create dictionary of branch index"""
    bDict = {}
    # create empy dictionaries for each scan bus
    for branch in mirror.Branch:
        bDict[str(branch.ScanBus)] ={}
        
    # add individual circuits to scanbus dicts
    for branch in mirror.Branch:
        bDict[str(branch.ScanBus)][branch.Ck] = branch

    return bDict