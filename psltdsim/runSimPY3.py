def runSimPY3(mirror, amqpAgent):
    """Python 3 side of LTD simulation"""
    print("*** runSimPY3 start")
    sim_start = time.time()
    PY3 = amqpAgent
    # Initialize PY3 specific Dynamics
    ltd.mirror.initPY3Dynamics(mirror)

    ## Already Happened
    ## calculate area f response characteristic (beta)
    #for area in mirror.Area:
    #    area.calcBeta()

    print("\n*** Starting Simulation (PY3)")
    # set flag for non-convergence
    mirror.sysCrash = False
    mirror.simRun = True

    # Init sim running vals
    for agent in mirror.Log:
        agent.initRunningVals()

    # Initalization value of Pe for [c_dp-1] functionality
    # NOTE: python does negative indexing, 
    # These values are appeneded now and popped once simulation ends
    mirror.r_ss_Pe.append(ltd.mirror.sumPe(mirror))
    mirror.r_ss_Pacc.append(0.0)
    mirror.r_f.append(1.0)
    mirror.r_fdot.append(0.0)

    # Start Simulation loop
    while (mirror.c_t <= mirror.endTime) and mirror.simRun:
        if mirror.debug:
            print("\n*** Data Point %d" % mirror.c_dp)
            print("*** Simulation time: %.2f" % (mirror.c_t))
        else:
            print("Simulation Time: %7.2f   " % mirror.c_t), # to print dots each step

        # Step System Wide dynamics
        ltd.mirror.combinedSwing(mirror, mirror.ss_Pacc)
        if mirror.c_f <= 0.0:
            # check for unreal frequency
            mirror.N = mirror.c_dp - 1
            mirror.sysCrash = True
            break;

        # Step Individual Agent Dynamics
        dynamic_start = time.time()
        for dynamicX in mirror.Dynamics:
            dynamicX.stepDynamics()
        mirror.DynamicTime += time.time()- dynamic_start

        # set pe = pm (dynamic action)
        for machineX in mirror.Machines:
            machineX.Pe = machineX.Pm
            # Send AMQP message to IPY (3/23/19 covers dynamic changes)
            send_start = time.time()
            PY3.send('toIPY',machineX.makeAMQPmsg())
            send_end = time.time()
            mirror.PY3SendTime += send_end-send_start
            mirror.PY3msgs+=1
            
        # Initialize Pertrubance delta
        mirror.ss_Pert_Pdelta = 0.0 # required for Pacc calculation
        mirror.ss_Pert_Qdelta = 0.0 # intended for system loss calculations

        # Step Perturbance Agents
        for pertX in mirror.Perturbance:
            if pertX.step():
                #if perturbance takes action, upday IPY
                send_start = time.time()
                PY3.send('toIPY', pertX.mObj.makeAMQPmsg())
                send_end = time.time()
                mirror.PY3SendTime += send_end-send_start
                mirror.PY3msgs+=1

        # Sum system loads to Account for any load changes from Perturbances
        mirror.ss_Pload, mirror.ss_Qload = ltd.mirror.sumLoad(mirror)

        # Sum current system Pm 
        mirror.ss_Pm = ltd.mirror.sumPm(mirror)
            
        # Calculate current system Pacc
        mirror.ss_Pacc = (
            mirror.ss_Pm 
            - mirror.r_ss_Pe[mirror.c_dp-1] # Most recent PSLF sum
            - mirror.ss_Pert_Pdelta
            )
            
        # Find current system Pacc Delta
        # NOTE: unused variable as of 2/2/19
        mirror.r_Pacc_delta[mirror.c_dp] = mirror.ss_Pacc - mirror.r_ss_Pacc[mirror.c_dp-1]

        Hmsg = {'msgType' : 'Handoff',
               'HandoffType': 'PY3toIPY',
               'Pacc':mirror.ss_Pacc,
               'Pert_Pdelta': mirror.ss_Pert_Pdelta,
               }
        PY3.send('toIPY', Hmsg)

        tic = time.time()
        PY3.receive('toPY3',PY3.redirect)
        mirror.PY3RecTime += time.time() - tic

        if mirror.sysCrash:
            # break out of while loop
            break

        # step log of Agents with ability
        for agentX in mirror.Log:
            agentX.logStep()

        # step time and data point
        mirror.r_t[mirror.c_dp] = mirror.c_t
        mirror.c_dp += 1
        mirror.c_t += mirror.timeStep

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
        for dyn in mirror.Dynamics:
            if dyn.appenedData:
                dyn.popUnsetData(mirror.c_dp)

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