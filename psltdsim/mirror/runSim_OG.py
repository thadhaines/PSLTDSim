def runSim_OG(mirror):
    """Ironpython only simulation run method from Mirror"""
    if not mirror.debug:
        # block pslf output for normal (non-debug) runs
        noPrintStr = "dispar[0].noprint = 1"
        PSLF.RunEpcl(noPrintStr)

    """Function to run LTD simulation"""
    print("\n*** Starting Simulation")
    # set flag for non-convergence
    sysCrash = 0

    # Initalization value of Pe for [c_dp-1] functionality
    # NOTE: python does negative indexing, 
    # These values are appeneded now and popped once simulation ends
    ltd.mirror.initRunningVals(mirror)
    mirror.r_ss_Pe.append(ltd.mirror.sumPe(mirror))
    mirror.r_ss_Pacc.append(0.0)
    mirror.r_f.append(1.0)
    mirror.r_fdot.append(0.0)

    # Step Initialize Dynamic Agents
    for x in range(len(mirror.Dynamics)):
            mirror.Dynamics[x].stepInitDynamics()

    # Start Simulation loop
    while mirror.c_t <= mirror.endTime:
        if mirror.debug:
            print("\n*** Data Point %d" % mirror.c_dp)
            print("*** Simulation time: %.2f" % (mirror.c_t))
        else:
            print("Simulation Time: %7.2f   " % mirror.c_t), # to print dots each step

        # Step System Wide dynamics
        ltd.mirror.combinedSwing(mirror, mirror.ss_Pacc)
        if mirror.c_f <= 0.0:
            # check for silly frequency
            N = mirror.c_dp - 1
            sysCrash = 1
            break;

        # Step Individual Agent Dynamics
        for x in range(len(mirror.Dynamics)):
            mirror.Dynamics[x].stepDynamics()

        # set pe = pm (dynamic action)
        for x in range(len(mirror.Machines)):
            mirror.Machines[x].Pe = mirror.Machines[x].Pm
            
        # Initialize Pertrubance delta
        mirror.ss_Pert_Pdelta = 0.0 # required for Pacc calculation
        mirror.ss_Pert_Qdelta = 0.0 # intended for system loss calculations

        # Step Perturbance Agents
        for x in range(len(mirror.Perturbance)):
            mirror.Perturbance[x].step()

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

        # Distribute Pacc to system machines Pe and solve PSLF
        try:
            ltd.mirror.distPe(mirror, mirror.ss_Pacc )
        # Check for convergence
        except ValueError as e:
            # Catches error thown for non-convergene
            print("*** Error Caught, Simulation Stopping...")
            print(e)
            # Pop void data from agents that log
            N = mirror.c_dp
            sysCrash = 1
            break;

        # update system Pe after PSLF power flow solution
        mirror.ss_Pe = ltd.mirror.sumPe(mirror)

        # step log of Agents with ability
        for x in range(len(mirror.Log)):
            mirror.Log[x].logStep()

        # step time and data point
        mirror.r_t[mirror.c_dp] = mirror.c_t
        mirror.c_dp += 1
        mirror.c_t += mirror.timeStep

    print("_______________________")
    print("    Simulation Complete\n")

    # remove initialization values
    if sysCrash == 1:
        for x in range(len(mirror.Log)):
                mirror.Log[x].popUnsetData(N)
    else:
        mirror.r_ss_Pe.pop(len(mirror.r_ss_Pe) -1)
        mirror.r_ss_Pacc.pop(len(mirror.r_ss_Pacc) -1)
        mirror.r_f.pop(len(mirror.r_f) -1)
        mirror.r_fdot.pop(len(mirror.r_fdot)-1)