def initPY3Dynamics(mirror):
    """Initialize PY3 specific Dynamics"""
    for gov in mirror.PSLFgov:
        # PSLF model information stored in mirror, each gov has a ref to mirror generator
        if gov.Type == 'tgov1':
            newLTDmod = ltd.dynamicAgents.tgov1Agent(mirror, gov)
            # attach dymanic models
            gov.Gen.gov.append(newLTDmod)
            mirror.Dynamics.append(newLTDmod)
            mirror.Log.append(newLTDmod)