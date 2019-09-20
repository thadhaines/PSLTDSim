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
    agentPSLFupdates = mirror.Machines + mirror.Bus +mirror.Load + mirror.Shunt + mirror.Branch + mirror.Area

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
            mirror.flatStart = 0
        # Check for convergence
        except ValueError as e:
            # Catches error thown for non-convergene
            print("*** Error Caught, Simulation Stopping...")
            print(e)
            sysCrash = True
            mirror.simRun = False
            break;

        # Using the msgGroup simParam and modulo to send messages
        msgcounter = 0
        msg = []
        for agent in agentPSLFupdates:
            # get new values from PSLF
            get_start = time.time()
            agent.getPvals()
            mirror.IPYPvalsTime += time.time() -get_start
            # append created AMQP msg to group message
            make_start = time.time()
            msg.append(agent.makeAMQPmsg())
            mirror.IPYmsgMake += time.time() - make_start

            msgcounter+=1

            if (msgcounter % mirror.IPYmsgGroup) == 0:
                # send message if group limit achieved
                send_start = time.time()
                IPY.send('toPY3', msg)
                mirror.IPYSendTime += time.time()-send_start
                sentMsgs +=1
                msg = []

        if len(msg) > 0:
            # send any group remainder messages
            send_start = time.time()
            IPY.send('toPY3', msg)
            mirror.IPYSendTime += time.time()-send_start
            sentMsgs +=1
        

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