def addPerturbance(mirror, tarType, idList, perType, perParams):
    """Add Perturbance to model.
    tarType = 'Load'
    idList = [Busnumber, id] id is optional, first object chosen by default
    perType = 'Step'
    perParams = list of specific perturbance parameters, will vary
        for a step: perParams = [targetAttr, tStart, newVal]
    NOTE: could be refactored to a seperate file
    TODO: Add other tarTypes ('Gen') and perTypes ('Ramp')
    Maybe rethink inputs as a dictionary?
    """

    #Locate target in mirror
    if tarType == 'Load':
        if len(idList) < 2:
            targetObj = ltd.find.findLoadOnBus(mirror, idList[0])
        else:
            targetObj = ltd.find.findLoadOnBus(mirror, idList[0], idList[1])

    #Create Perturbance Agent
    if (perType == 'Step') and targetObj:
        # perParams = [targetAttr, tStart, newVal, type='r']
        newStepAgent = ltd.perturbanceAgents.LoadStepAgent(mirror, targetObj, perParams)
        mirror.Perturbance.append(newStepAgent)
        print("*** Perturbance Agent added!")
        print(newStepAgent)
        return

    print("*** Perturbance Agent error - nothing added.")