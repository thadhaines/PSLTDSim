def runSim_IPY(mirror, amqpAgent):
    """Ironpython side of LTD simulation"""
    print("*** runSim_IPY start")
    # Initialization variables
    IPY = amqpAgent
    mirror.simRun = True
    mirror.ss_Pe = ltd.mirror.sumPe(mirror)
    mirror.ss_Pload = ltd.mirror.sumLoad(mirror)[0]
    IPYSendTime = 0.0
    sentMsgs = 0
    sysCrash = False
    if not mirror.debug:
        # block pslf output for normal (non-debug) runs
        noPrintStr = "dispar[0].noprint = 1"
        PSLF.RunEpcl(noPrintStr)

    # handle AMQP messages and update mir/PSLF accordingly
    IPY.receive('toIPY',IPY.redirect)
    agentPSLFupdates = mirror.Machines + mirror.Bus +mirror.Load

    ## enter some while loop for simulation run
    while mirror.simRun:
        # received Handoff and Pacc Verified - else error in handoff
        tic = time.time()
        for agent in agentPSLFupdates:
            agent.setPvals()
        mirror.IPYPvalsTime += time.time() - tic
            
        # distPe loop thing (which is really distributes Pacc)
        try:
            ltd.mirror.distPacc(mirror, mirror.ss_Pacc )
        # Check for convergence
        except ValueError as e:
            # Catches error thown for non-convergene
            print("*** Error Caught, Simulation Stopping...")
            print(e)
            sysCrash = True
            mirror.simRun = False
            break;

        # send new values to PY3
        get_start = time.time()
        for agent in agentPSLFupdates:
            agent.getPvals()
            
        make_start = time.time()
        machMsg = ltd.amqp.makeGroupMsg(mirror.Machines)
        busMsg = ltd.amqp.makeGroupMsg(mirror.Bus)
        loadMsg = ltd.amqp.makeGroupMsg(mirror.Load)

        send_start = time.time()
        IPY.send('toPY3', machMsg)
        IPY.send('toPY3', busMsg)
        IPY.send('toPY3', loadMsg)

        send_end = time.time()
        mirror.IPYPvalsTime += make_start -get_start
        mirror.IPYmsgMake += send_start - make_start
        mirror.IPYSendTime += send_end-send_start
        sentMsgs +=3

        # send hand off of Sum Pe
        mirror.ss_Pe = ltd.mirror.sumPe(mirror)
        pload = ltd.mirror.sumLoad(mirror)[0]
        Hmsg = {'msgType' : 'Handoff',
               'HandoffType': 'IPYtoPY3',
               'ss_Pe': mirror.ss_Pe,
               'pload' : pload,
               'PFTime' :mirror.PFTime,
               'PFSolns' : mirror.PFSolns,
               'SentMsg' : sentMsgs,
               'IPYmsgMake': mirror.IPYmsgMake,
               'IPYSendTime' : mirror.IPYSendTime,
               'IPYdistPaccTime' : mirror.IPYdistPaccTime,
               'IPYPvalsTime' : mirror.IPYPvalsTime,
               'IPYFindTime' : mirror.FindTime,
               }
        #print('msg sending %.2f\t%.2f' %(sentMsgs, IPYSendTime))
        IPY.send('toPY3',Hmsg)

        # receive at end to enable endSim AMQP message
        IPY.receive('toIPY',IPY.redirect)

    if sysCrash:
        Hmsg = {'msgType' : 'SysCrash',
               }
        IPY.send('toPY3',Hmsg)
    else:
        print("*** runSim_IPY end")