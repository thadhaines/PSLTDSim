def createPY3DynamicAgents(mirror):
    """Initialize PY3 specific Dynamics"""
    for gov in mirror.PSLFgov:
        # PSLF model information stored in mirror, each gov has a ref to mirror generator
        modFound = 0

        if gov.Type.lower() == 'tgov1':
            newLTDmod = ltd.dynamicAgents.tgov1Agent(mirror, gov)
            modFound = 1

        # TODO: Implement generic governors for unmodeled governors - probably base off inertia or something?

        if modFound:
            # attach dymanic model to mirror agents and system collections
            gov.Gen.gov_model = newLTDmod
            gov.Gen.cv['IRPflag'] = True #
            mirror.Dynamics.append(newLTDmod)
            mirror.Log.append(newLTDmod)

