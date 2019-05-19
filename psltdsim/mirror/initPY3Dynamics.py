def initPY3Dynamics(mirror):
    """Initialize PY3 specific Dynamics"""
    for gov in mirror.PSLFgov:
        # PSLF model information stored in mirror, each gov has a ref to mirror generator
        modFound = 0

        if gov.Type.lower() == 'tgov1':
            newLTDmod = ltd.dynamicAgents.tgov1Agent(mirror, gov)
            modFound = 1

        if gov.Type.lower() == 'ggov1':
            newLTDmod = ltd.dynamicAgents.ggov1Agent(mirror, gov)
            modFound = 1

        if modFound:
            # attach dymanic model to mirror agents and system collections
            gov.Gen.gov_model = newLTDmod
            mirror.Dynamics.append(newLTDmod)
            mirror.Log.append(newLTDmod)

    for dynamic in mirror.Dynamics:
        dynamic.stepInitDynamics()