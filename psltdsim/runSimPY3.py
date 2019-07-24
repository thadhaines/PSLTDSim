def runSimPY3(mirror, amqpAgent):
    """Python 3 side of LTD simulation"""
    print("*** runSimPY3 start")
    PY3 = amqpAgent


    # Initialize PY3 specific Dynamics
    ltd.mirror.initPY3Dynamics(mirror)

    # calculates all area P (required for IC init)
    ltd.mirror.sumLoad(mirror) 
    ltd.mirror.sumPe(mirror)

    # calculate area f response characteristic (beta), and interchange ( IC )
    for area in mirror.Area:
        area.calcBeta()
        area.initIC()

    # Place for user input 'code' to be run (timer defs, pp, BA, DTC, etc... )
    mirror.ppDict = {}
    if 'ltdPath' in mirror.locations:
        exec(open(mirror.locations['ltdPath']).read());

    # parse LTD to handle perturbances
    if hasattr(mirror, 'sysPerturbances'):
        ltd.parse.parseLtd(mirror, mirror.sysPerturbances)

    # if defined Power Plants, pass each entry to agent class
    if hasattr(mirror, 'sysPowerPlants'):
        for name in mirror.sysPowerPlants:
            ltd.systemAgents.PowerPlantAgent(mirror, name, mirror.sysPowerPlants[name])

    # Create any defined Balancing Authorities
    if hasattr(mirror, 'sysBA'):
        for name in mirror.sysBA:
            BAtype = mirror.sysBA[name]['Type'].split(":")[0].strip()
            if BAtype.lower() == 'tlb':
                ltd.BAAgents.TLB(mirror, name, mirror.sysBA[name])
        # Add BAs to Log
        mirror.Log += mirror.BA

    # Create Timers # NOTE: more of a debug than a useful thing -> Timers will be created by DTC
    """
    if hasattr(mirror, 'TimerInput'):
        for timer in mirror.TimerInput:
            ltd.systemAgents.TimerAgent(mir,timer, mirror.TimerInput[timer]) 
    """

    print("\n*** Starting Simulation (PY3)")
    sim_start = time.time()
    # set flag for non-convergence
    mirror.sysCrash = False
    mirror.simRun = True

    # Init sim running vals
    for agent in mirror.Log:
        agent.initRunningVals()

    # Initalization value of Pe for [...cv['dp']-1] functionality
    # NOTE: python does negative indexing, 
    # These values are appeneded now and popped once simulation ends
    mirror.r_ss_Pe.append(ltd.mirror.sumPe(mirror))
    mirror.r_ss_Pacc.append(0.0)
    mirror.r_f.append(1.0)
    mirror.r_fdot.append(0.0)

    # Start Simulation loop
    while (mirror.cv['t'] <= mirror.endTime) and mirror.simRun:
        if mirror.debug:
            print("\n*** Data Point %d" % mirror.cv['dp'])
            print("*** Simulation time: %.2f" % (mirror.cv['t']))
        else:
            #print("Simulation Time: %7.2f   " % mirror.cv['t']), # to print dots each step
            print("Simulation Time:%4d Minutes%3d Seconds   " % (mirror.cv['t']//60, mirror.cv['t']%60 ) ), # to print dots each step

        # Step System Wide dynamics
        ltd.mirror.combinedSwing(mirror, mirror.ss_Pacc)
        if mirror.cv['f'] <= 0.0:
            # check for unreal frequency
            mirror.N = mirror.cv['dp'] - 1
            mirror.sysCrash = True
            break;

        # Calculate SCE
        # NOTE: Not really SCE -> eqution needs reworking...
        for mach in mirror.Machines:
            mach.calcSCE()
        
        # Calculate Interchange and Station Control error for all areas
        for area in mirror.Area:
            area.sumSCE()
            area.calcICerror()

        # Calculate ACE (BA step)
        for ba in mirror.BA:
            ba.step()
        # Step any created AGC ramps
        for AGCramp in mirror.AGCramp:
            AGCramp.step()

        # Step Timers (should probably happen when Time is stepped [below...])

        # Step Definite Time Controllers

        # Step Individual Agent Dynamics
        dynamic_start = time.time()
        for dynamicX in mirror.Dynamics:
            dynamicX.stepDynamics()
        mirror.DynamicTime += time.time()- dynamic_start

        # Send grouped AMQP messages to IPY (3/23/19 covers dynamic changes)
        msgcounter = 0
        msg = []
        # set pe = pm (dynamic action)
        for machineX in mirror.Machines:
            machineX.cv['Pe'] = machineX.cv['Pm']            
            msg.append(machineX.makeAMQPmsg())
            msgcounter+=1

            if (msgcounter % mirror.PY3msgGroup) == 0:
                # send message if group limit achieved
                send_start = time.time()
                PY3.send('toIPY', msg)
                mirror.PY3SendTime += time.time()-send_start
                mirror.PY3msgs +=1
                msg = [] # reset msg

        if len(msg) > 0:
            # send any group remainder messages
            send_start = time.time()
            PY3.send('toIPY', msg)
            mirror.PY3SendTime += time.time()-send_start
            mirror.PY3msgs +=1

        # Initialize Pertrubance delta
        mirror.ss_Pert_Pdelta = 0.0 # required for Pacc calculation
        mirror.ss_Pert_Qdelta = 0.0 # intended for system loss calculations

        # Step Perturbance Agents and AGC ramps
        for pertX in mirror.Perturbance:
            if pertX.step():
                #if perturbance takes action, upday IPY
                send_start = time.time()
                PY3.send('toIPY', pertX.mObj.makeAMQPmsg())
                mirror.PY3SendTime += time.time() -send_start
                mirror.PY3msgs+=1

        # Sum system loads to Account for any load changes from Perturbances
        mirror.ss_Pload, mirror.ss_Qload = ltd.mirror.sumLoad(mirror)

        # Sum current system Pm 
        mirror.ss_Pm = ltd.mirror.sumPm(mirror)
            
        # Calculate current system Pacc
        mirror.ss_Pacc = (
            mirror.ss_Pm 
            - mirror.r_ss_Pe[mirror.cv['dp']-1] # Most recent PSLF sum
            - mirror.ss_Pert_Pdelta
            )
            
        # Find current system Pacc Delta....
        # NOTE: unused variable as of 2/2/19 -> if div by ts= Pacc dot... i.e. Jerk...
        mirror.r_Pacc_delta[mirror.cv['dp']] = mirror.ss_Pacc - mirror.r_ss_Pacc[mirror.cv['dp']-1]

        Hmsg = {'msgType' : 'Handoff',
               'HandoffType': 'PY3toIPY',
               'Pacc':mirror.ss_Pacc,
               'Pert_Pdelta': mirror.ss_Pert_Pdelta,
               'flatStart' : mirror.flatStart,
               }
        PY3.send('toIPY', Hmsg)
        mirror.flatStart = 0
        tic = time.time()
        PY3.receive('toPY3',PY3.redirect)
        mirror.PY3RecTime += time.time() - tic

        if mirror.sysCrash:
            # break out of while loop
            break

        # Step timers
        for timerName in mirror.Timer:
            mirror.Timer[timerName].step()

        # step log of Agents with ability
        for agent in mirror.Log:
            agent.logStep()

        # step time and data point
        mirror.r_t[mirror.cv['dp']] = mirror.cv['t']
        mirror.cv['dp'] += 1
        mirror.cv['t'] += mirror.timeStep

    print("_______________________")
    print("    Simulation Complete\n")
    sim_end = time.time()
    mirror.SimTime = sim_end-sim_start
    # remove initialization values
    if mirror.sysCrash:
        for agentX in mirror.Log:
            agentX.popUnsetData(mirror.N)
    else:
        mirror.r_ss_Pe.pop(len(mirror.r_ss_Pe) -1)
        mirror.r_ss_Pacc.pop(len(mirror.r_ss_Pacc) -1)
        mirror.r_f.pop(len(mirror.r_f) -1)
        mirror.r_fdot.pop(len(mirror.r_fdot)-1)

        # Handle appeneded data in dynamic models
        for agent in (mirror.Dynamics + mirror.Filter):
            if agent.appenedData:
                agent.popUnsetData(mirror.cv['dp'])

    if not mirror.sysCrash:
        PY3.send('toIPY',{'msgType' : 'endSim'})
    else:
        print("*** runSimPY3 end")

    # Data Export
    if mirror.simParams['exportFinalMirror']:
        mirror.simParams['fileName'] += 'F'
        ltd.data.saveMirror(mirror, mirror.simParams)

    if mirror.simParams['exportMat']:
        ltd.data.exportMat(mirror, mirror.simParams)

    print("_______________________") # the bottom line
    print("   Data Export Complete")