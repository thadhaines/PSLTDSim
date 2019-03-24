def addPerturbance(mirror, tarType, idList, perType, perParams):
    """Add Perturbance to model.
    tarType = 'Load'
    idList = [Busnumber, id] id is optional, first object chosen by default
    perType = 'Step'
    perParams = list of specific perturbance parameters, will vary
        for a step: perParams = [targetAttr, tStart, newVal]

    TODO: Add other tarTypes ('Gen') and perTypes ('Ramp')
    Maybe rethink inputs as a dictionary?
    """
    targetObj= None

    #Locate target in mirror
    if tarType.lower() == 'load':
        if len(idList) < 2:
            targetObj = ltd.find.findLoadOnBus(mirror, idList[0])
        else:
            targetObj = ltd.find.findLoadOnBus(mirror, idList[0], idList[1])

    #Create Perturbance Agent
    if (perType.lower() == 'step') and targetObj:
        # perParams = [targetAttr, tStart, newVal, type='r']
        newStepAgent = ltd.perturbanceAgents.LoadStepAgent(mirror, targetObj, perParams)
        mirror.Perturbance.append(newStepAgent)
        print("*** Perturbance Agent added!")
        print(newStepAgent)
        return

    if (perType.lower() == 'ramp') and targetObj:
        # perParams = [targetAttr, tStart, RAtime, RAVal, holdTime, RBtime, RBVal]
        newRampAgent = ltd.perturbanceAgents.LoadRampAgent(mirror, targetObj, perParams)
        mirror.Perturbance.append(newRampAgent)
        print("*** Perturbance Agent added!")
        print(newRampAgent)
        return

    print("*** Perturbance Agent error - nothing added.")