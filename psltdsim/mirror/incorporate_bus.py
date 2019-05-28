def incorporate_bus(mirror, newBus, areaAgent):
    """Handles adding Busses and associated children to Mirror"""
    # b_ .. Bus objects
    # c_ .. Current Object
    # m_ .. model
    mir = mirror # to simplify referencing
    slackFlag = 0
    if newBus.Type == 0:
        slackFlag = 1

    newBusAgent = ltd.systemAgents.BusAgent(mir, newBus)

    # locate and create generators on bus
    if (newBusAgent.Ngen > 0):
        b_gen = col.GeneratorDAO.FindByBus(newBusAgent.Scanbus)
        for c_gen in range(newBusAgent.Ngen):

            if slackFlag:
                newGenAgent = ltd.systemAgents.SlackAgent(mir, newBusAgent, b_gen[c_gen])
                # add references to slack gen in bus, mirror, and area
                newBusAgent.Slack.append(newGenAgent)
                mirror.Slack.append(newGenAgent)
                areaAgent.Slack.append(newGenAgent)
            else:
                newGenAgent = ltd.systemAgents.GeneratorAgent(mir, newBusAgent, b_gen[c_gen])
                # add references to gen in bus, mirror, and area
                newBusAgent.Gens.append(newGenAgent)
                mirror.Gens.append(newGenAgent)
                areaAgent.Gens.append(newGenAgent)

    # locate and create loads on bus
    if newBusAgent.Nload > 0:
        b_load = col.LoadDAO.FindByBus(newBusAgent.Scanbus)
        for c_load in range(newBusAgent.Nload):
            newLoadAgent = ltd.systemAgents.LoadAgent(mir, newBusAgent, b_load[c_load])
            # add references to load in bus, and area
            newBusAgent.Load.append(newLoadAgent)
            mirror.Load.append(newLoadAgent)
            areaAgent.Load.append(newLoadAgent)
    
    # locate and create shunts on bus
    if newBusAgent.Nshunt > 0:
        b_shunts = col.ShuntDAO.FindAnyShuntsByBus(newBusAgent.Scanbus)
        for c_shunt in b_shunts:
            newShuntAgent = ltd.systemAgents.ShuntAgent(mir, newBusAgent, c_shunt)
            # add references to shunt in bus, mirror and area 
            newBusAgent.Shunt.append(newShuntAgent)
            mirror.Shunt.append(newShuntAgent)
            areaAgent.Shunt.append(newShuntAgent)

    mirror.Bus.append(newBusAgent)
    areaAgent.Bus.append(newBusAgent)