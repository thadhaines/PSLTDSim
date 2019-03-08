def incorporate_bus(mirror, newBus, areaAgent):
    """Handles adding Busses and associated children to Mirror"""
    # b_ .. Bus objects
    # c_ .. Current Object
    # m_ .. model
    m_ref = areaAgent.model # to simplify referencing
    slackFlag = 0
    if newBus.Type == 0:
        slackFlag = 1

    newBusAgent = ltd.systemAgents.BusAgent(m_ref, newBus)

    # locate and create bus generator children
    if (newBusAgent.Ngen > 0):
        b_gen = col.GeneratorDAO.FindByBus(newBusAgent.Scanbus)
        for c_gen in range(newBusAgent.Ngen):

            if slackFlag:
                newGenAgent = ltd.systemAgents.SlackAgent(m_ref, newBusAgent, b_gen[c_gen])
                # add references to gen in model and bus,area agent
                newBusAgent.Slack.append(newGenAgent)
                mirror.Slack.append(newGenAgent)
                areaAgent.Slack.append(newGenAgent)
            else:
                newGenAgent = ltd.systemAgents.GeneratorAgent(m_ref, newBusAgent, b_gen[c_gen])
                # add references to gen in model and bus,area agent
                newBusAgent.Gens.append(newGenAgent)
                mirror.Gens.append(newGenAgent)
                areaAgent.Gens.append(newGenAgent)

    # locate and create bus load children
    if newBusAgent.Nload > 0:
        b_load = col.LoadDAO.FindByBus(newBusAgent.Scanbus)
        for c_load in range(newBusAgent.Nload):
            newLoadAgent = ltd.systemAgents.LoadAgent(m_ref, newBusAgent, b_load[c_load])
            # add references to load in model and bus,area agent
            newBusAgent.Load.append(newLoadAgent)
            mirror.Load.append(newLoadAgent)
            areaAgent.Load.append(newLoadAgent)

    mirror.Bus.append(newBusAgent)
    areaAgent.Bus.append(newBusAgent)