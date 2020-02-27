def findBranchByFTC(mirror, idList):
    """Locate mirror branch agent by idList which contatins:
    [FromBus, ToBus, CircuitId]
    Pretty lazy approach 'ok' - only has to find once, then uses scanbus
    - in other words - room for improvement....
    """

    for branch in mirror.Branch:
        if branch.Bus.Extnum == int(idList[0]):
            if branch.TBus.Extnum == int(idList[1]):
                if branch.Ck == idList[2]:
                    return branch

    # branch not found
    print('*** Branch from %d to %d with id %s not found.'
          %(idList[0], idList[1], idList[2]))
    return None