def addPerturbance(mirror, tarType, idList, perType, perParams):
    """Add Perturbance to model.
    tarType = 'load', 'gen', 'shunt'
    idList = [Busnumber, id] id is optional, first object chosen by default
    perType = 'step', 'ramp'
    perParams = list of specific perturbance parameters, will vary
        for a step: perParams = [targetAttr, tStart, newVal]

    TODO: Maybe rethink inputs as a dictionary?
    """

    targetObj = ltd.find.findAgent(mirror, tarType, idList)
    
    #Create Perturbance Agent
    if (perType.lower() == 'step') and targetObj:
        # perParams = [targetAttr, tStart, newVal, type='r']
        newStepAgent = ltd.perturbance.StepAgent(mirror, targetObj, tarType, perParams)
        if newStepAgent.ProcessFlag:
            mirror.Perturbance.append(newStepAgent)
            print("*** Perturbance Agent added:")
            print(newStepAgent)
            return

    if (perType.lower() == 'ramp') and targetObj:
        # perParams = [targetAttr, tStart, RAtime, RAVal, holdTime, RBtime, RBVal]
        newRampAgent = ltd.perturbance.RampAgent(mirror, targetObj, tarType, perParams)
        mirror.Perturbance.append(newRampAgent)
        print("*** Perturbance Agent added:")
        print(newRampAgent)
        return

    print("*** Perturbance Agent error - nothing added.")