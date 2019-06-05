def distPacc(mirror, deltaPacc):
    """Distribute Pe among generators until global slack error below tolerance.
    Adjust to account for all slack errors?
    Assumes:
        Each system has only 1 slack bus
        Each area has it's own designated slack gen

    NOTE: pretty rough on the mulitple slack generator handling (i.e. untested)
    TODO: account for status, IRP_flag, and mw limits of generators (Pmax)
    """

    tol_Flag = 1 # goes to zero once error < tolerance

    tol = mirror.slackTol
    error = tol + 1
    Hsys = mirror.ss_H # MW*sec
    Pacc = deltaPacc
    iteration = 1

    while tol_Flag:
        tic1 = time.time()
        if mirror.debug:
            print("*** LTD: Distributing %.2f MW of Pacc, Iteration %d" % (Pacc, iteration))
        #for each system area:
        for c_gen in mirror.Machines:

            # Ensure off generators don't suppy power
            if c_gen.cv['St'] == 0:
                c_gen.cv['Pe'] = 0
                c_gen.setPvals()
                continue

            if c_gen.globalSlack:
                if iteration == 1:
                    #distribute to slack on First pass 
                    c_gen.cv['Pe'] = c_gen.cv['Pe'] - Pacc * (c_gen.H/Hsys)
                    # Set Pe_calc
                    c_gen.cv['Pe_calc'] = c_gen.cv['Pe'] 
                else:
                    # On later iterations, Reset generator to estimated value
                    c_gen.cv['Pe'] = c_gen.cv['Pe_calc']
            
                # Update PSLF values
                c_gen.setPvals()
                c_gen.Bus.setPvals()

            #Distribute delta Pacc to non slack other gens
            else:
                c_gen.cv['Pe'] = c_gen.cv['Pe'] - Pacc * (c_gen.H/Hsys) 
                c_gen.setPvals()
                c_gen.Bus.setPvals()

        toc1 = time.time()
        # Pe is distributed to all generators in all areas, solve Power flow
        ltd.mirror.LTD_SolveCase(mirror)

        #update mirror timers
        mirror.IPYdistPaccTime += toc1-tic1
        #mirror.IPYPvalsTime += toc2-tic2

        # Calculate global slack error (could be an average in the future?)
        mirror.globalSlack.getPvals()
        error = mirror.globalSlack.cv['Pe_calc'] - mirror.globalSlack.cv['Pe'] 
        
        if mirror.debug:
            print('expected: %.2f\tactual: %.2f\terror: %.2f' 
                  % (mirror.globalSlack.cv['Pe_calc'], mirror.globalSlack.cv['Pe'], error))

        # exit while loop if tolerance met
        if abs(error) <= tol:
            mirror.globalSlack.cv['Pe_error'] = error
            tol_Flag = 0
            continue

        # tolerance not met, redistribute error
        Pacc = error
        iteration +=1

    tic2 = time.time()
    #Update mirror machines with PSLF values from power flow solution
    for gen in mirror.Machines:
        gen.getPvals()
    toc2 = time.time()
    mirror.IPYPvalsTime += toc2-tic2
