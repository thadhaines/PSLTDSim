def makeBranchDict(mirror):
    """Create dictionary of branch index"""
    bDict = {}
    for branch in mirror.Branch:
        bDict[str(branch.ScanBus)] = branch

    return bDict