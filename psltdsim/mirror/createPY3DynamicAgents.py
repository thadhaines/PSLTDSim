def createPY3DynamicAgents(mirror):
    """Initialize PY3 specific Dynamics"""
    mirror.zeroRmodels = []
    for gov in mirror.PSLFgov:


        if gov.Gen == None:
            # for governor models that aren't associated to a known generator
            continue

        if gov.R == 0.0:
            # ignor models with a zero R
            mirror.zeroRmodels.append(gov.dydLine)
            continue

        # PSLF model information stored in mirror, each gov has a ref to mirror generator
        modFound = 0

        # TODO: Implement generic governors for unmodeled governors & Further work to cast to certain types
        if gov.isGeneric:
            if gov.TurbineType =='steam':
                newLTDmod = ltd.dynamicAgents.genericSteamGovAgent(mirror, gov)
                modFound = 1
            elif gov.TurbineType =='general': # casting general turbines to gas
                newLTDmod = ltd.dynamicAgents.genericGasGovAgent(mirror, gov)
                modFound = 1
            elif gov.TurbineType =='hydro':
                newLTDmod = ltd.dynamicAgents.genericHydroGovAgent(mirror, gov)
                modFound = 1
            
        elif (gov.Type.lower() == 'tgov1'):
            newLTDmod = ltd.dynamicAgents.tgov1Agent(mirror, gov)
            modFound = 1

        if modFound:
            # attach dymanic model to mirror agents and system collections
            gov.Gen.gov_model = newLTDmod
            gov.Gen.cv['IRPflag'] = True #
            mirror.Dynamics.append(newLTDmod)
            mirror.Log.append(newLTDmod)

