def findAgent(mirror, tarType, idList):
    """Function to return mirror agent reference for a variety of types"""
    targetObj= None

    #Locate target in mirror
    if tarType.lower() == 'mirror':
        targetObj = mirror

    if tarType.lower() == 'bus':
        targetObj = ltd.find.findBus(mirror, idList[0])

    if tarType.lower() == 'load':
        if len(idList) < 2:
            targetObj = ltd.find.findLoadOnBus(mirror, idList[0])
        else:
            targetObj = ltd.find.findLoadOnBus(mirror, idList[0], idList[1])

    if tarType.lower() == 'gen':
        if len(idList) < 2:
            targetObj = ltd.find.findGenOnBus(mirror, idList[0])
        else:
            targetObj = ltd.find.findGenOnBus(mirror, idList[0], idList[1])

    if (tarType.lower() == 'shunt') or (tarType.lower() == 'cap'):
        if len(idList) < 2:
            targetObj = ltd.find.findShuntOnBus(mirror, idList[0])
        else:
            targetObj = ltd.find.findShuntOnBus(mirror, idList[0], idList[1])
              
    if tarType.lower() == 'branch':
        # Branches must have from, to, and ck id
        targetObj = ltd.find.findBranchByTFC(mirror, idList)

    return targetObj