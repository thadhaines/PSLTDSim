def distPe(model, deltaPacc):
    """Distribute Pe among generators until global slack error below tolerance.
    Could be altered later to account for all slack errors.
    Assumes:
        Eeach area has 1 slack generator
        Each system has 1 global slack generator

    NOTE: pretty rough on the mulitple slack generator handling (i.e. untested)
    TODO: account for status, IRP_flag, and mw limits of generators
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
        print("Distributing %.2f MW of Pacc, Iteration %d" % (Pacc, iteration))
        #for each model area:
        for c_area in range(len(model.Area)):
            if fp_Flag:
                #distribute to slack on First pass and set Pe_calc
                model.Area[c_area].Slack[0].Pe = ( 
                    model.Area[c_area].Slack[0].Pe - Pacc*(model.Area[c_area].Slack[0].H/Hsys)
                    )
                model.Area[c_area].Slack[0].Pe_calc = model.Area[c_area].Slack[0].Pe
                model.Area[c_area].Slack[0].setPvals()

            else:
                # Reset slack generators to estimated value
                model.Area[c_area].Slack[0].Pe = model.Area[c_area].Slack[0].Pe_calc      
                model.Area[c_area].Slack[0].setPvals()

            #Distribute delta Pacc to all non-slack gens in area
            gens = model.Area[c_area].Gens

            for c_gen in range(len(gens)):
                gens[c_gen].Pe = gens[c_gen].Pe - Pacc * (gens[c_gen].H/Hsys)
                gens[c_gen].setPvals()

        fp_Flag = 0
        # Pe is distributed to all generators in all areas, solve Power flow
        model.LTD_Solve()
        #Update mirror with Pe from power flow solution
        for gen in range(len(model.Machines)):
            model.Machines[gen].getPvals()

        # Calculate global slack error (could be an average in the future?)
        error = globalSlack.Pe - globalSlack.Pe_calc
        
        # exit while loop if tolerance met
        if abs(error) < tol:
            globalSlack.Pe_error = error
            tol_Flag = 0
            continue

        # tolerance not met, redistribute error
        Pacc = error
        iteration +=1