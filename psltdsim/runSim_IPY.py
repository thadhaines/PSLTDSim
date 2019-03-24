def runSim_IPY(mirror, amqpAgent):
    """Ironpython side of LTD simulation"""
    print("this is runSim_IPY")
    # Initialization variables
    IPY = amqpAgent
    mirror.simRun = True
    mirror.ss_Pe = ltd.mirror.sumPe(mirror)
    mirror.ss_Pload = ltd.mirror.sumLoad(mirror)[0]

    if not mirror.debug:
        # block pslf output for normal (non-debug) runs
        noPrintStr = "dispar[0].noprint = 1"
        PSLF.RunEpcl(noPrintStr)

    # handle AMQP messages and update mir/PSLF accordingly
    IPY.receive('toIPY',IPY.redirect)
    agentPSLFupdates = mirror.Machines + mirror.Load + mirror.Bus

    ## enter some while loop for simulation run
    while mirror.simRun:
        # received Handoff and Pacc Verified - else error in handoff
        for agent in agentPSLFupdates:
            agent.setPvals()
        # distPe loop thing (which is really distributes Pacc)
        try:
            ltd.mirror.distPacc(mirror, mirror.ss_Pacc )
        # Check for convergence
        except ValueError as e:
            # Catches error thown for non-convergene
            print("*** Error Caught, Simulation Stopping...")
            print(e)
            # Pop void data from agents that log
            N = mirror.c_dp
            sysCrash = 1
            # TODO send sys crash AMQP to PY3
            break;

        # send new values to PY3
        for agent in agentPSLFupdates:
            agent.getPvals()
            IPY.send('toPY3', agent.makeAMQPmsg())
        # send hand off of Sum Pe
        mirror.ss_Pe = ltd.mirror.sumPe(mirror)
        pload = ltd.mirror.sumLoad(mirror)[0]
        Hmsg = {'msgType' : 'Handoff',
               'HandoffType': 'IPYtoPY3',
               'ss_Pe': mirror.ss_Pe,
               'pload' : pload,
               }
        IPY.send('toPY3',Hmsg)
        # receive at end to enable endSim AMQP message
        IPY.receive('toIPY',IPY.redirect)

    print("this is runSim_IPY end")