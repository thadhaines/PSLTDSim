def distPe(model, deltaPacc):
    """Distribute Pe among generators until global slack error below tolerance.
    Could be altered later to account for all slack errors.
    Assumes:
        Eeach area has 1 slack generator
        Each system has 1 global slack generator

    NOTE: pretty rough on the mulitple slack generator handling (i.e. untested)
    TODO: account for status, IRP_flag, and mw limits of generators (Pmax)
    """
    fp_Flag = 1
    tol_Flag = 1 # goes to zero once error < tolerance

    tol = model.slackTol
    error = tol + 1
    Hsys = model.ss_H # MW*sec
    Pacc = deltaPacc
    iteration = 1

    # create reference to global slack gen
    for gen in range(len(model.Slack)):
        if model.Slack[gen].globalSlack:
            globalSlack = model.Slack[gen]

    while tol_Flag:
        print("*** LTD: Distributing %.2f MW of Pacc, Iteration %d" % (Pacc, iteration))
        #for each model area:
        for c_area in range(len(model.Area)):
            if fp_Flag:
                #distribute to slack on First pass and set Pe_calc
                slackPacc = Pacc*(model.Area[c_area].Slack[0].H/Hsys)
                model.Area[c_area].Slack[0].Pe = model.Area[c_area].Slack[0].Pe - slackPacc 
                model.Area[c_area].Slack[0].Pe_calc = model.Area[c_area].Slack[0].Pe
                model.Area[c_area].Slack[0].setPvals()
                # remove handled Pacc from rest of system distribution
                Pacc = Pacc - slackPacc
                # create new H without slack gen to distribute to
                HsysDist = Hsys - model.Area[c_area].Slack[0].H
                fp_Flag = 0

            else:
                # Reset slack generators to estimated value
                model.Area[c_area].Slack[0].Pe = model.Area[c_area].Slack[0].Pe_calc      
                model.Area[c_area].Slack[0].setPvals()

            #list of all non slack machines
            gens = model.Area[c_area].Gens

            #Distribute delta Pacc to all non-slack gens in area
            for c_gen in range(len(gens)):
                gens[c_gen].Pe = gens[c_gen].Pe - Pacc * (gens[c_gen].H/HsysDist) 
                gens[c_gen].setPvals()
                # ensure Vsched in PSLF is correct
                gens[c_gen].Bus.setPvals()

        # Pe is distributed to all generators in all areas, solve Power flow
        model.LTD_Solve()

        #Update mirror with Pe from power flow solution
        for gen in range(len(model.Machines)):
            model.Machines[gen].getPvals()

        # Calculate global slack error (could be an average in the future?)
        error = globalSlack.Pe_calc - globalSlack.Pe 
        
        if model.debug:
            print('expected: %.2f\tactual: %.2f\terror: %.2f' % (globalSlack.Pe_calc, globalSlack.Pe, error) )

        # exit while loop if tolerance met
        if abs(error) <= tol:
            globalSlack.Pe_error = error
            tol_Flag = 0
            continue

        # tolerance not met, redistribute error
        Pacc = error
        iteration +=1