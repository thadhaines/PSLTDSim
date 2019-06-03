def distPacc(mirror, deltaPacc):
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

    tol = mirror.slackTol
    error = tol + 1
    Hsys = mirror.ss_H # MW*sec
    Pacc = deltaPacc
    iteration = 1

    while tol_Flag:
        tic1 = time.time()
        if mirror.debug:
            print("*** LTD: Distributing %.2f MW of Pacc, Iteration %d" % (Pacc, iteration))
        #for each mirror area:
        for c_area in mirror.Area:
            if iteration == 1:
                #distribute to slack on First pass and set Pe_calc
                slackPacc = Pacc*(c_area.AreaSlack.H/Hsys)
                c_area.AreaSlack.Pe -= slackPacc 

                # Estimated Pe post PF soln
                c_area.AreaSlack.Pe_calc = c_area.AreaSlack.Pe 
                c_area.AreaSlack.setPvals()

                # remove handled Pacc from rest of system distribution
                Pacc = Pacc - slackPacc
                # create new H without slack gen to distribute to
                HsysDist = Hsys - c_area.AreaSlack.H

            else:
                # Reset slack generators to estimated value
                c_area.AreaSlack.Pe = c_area.AreaSlack.Pe_calc
                c_area.AreaSlack.setPvals()

            #Distribute delta Pacc to all other gens in area
            for c_gen in c_area.Machines:
                if not c_gen.areaSlack:
                    c_gen.Pe = c_gen.Pe - Pacc * (c_gen.H/HsysDist) 
                    c_gen.setPvals()
                    # ensure Vsched in PSLF is correct
                    c_gen.Bus.setPvals()


        toc1 = time.time()
        # Pe is distributed to all generators in all areas, solve Power flow
        ltd.mirror.LTD_SolveCase(mirror)
        
        """
        # moved outside loop to fully get PSLF values only after slack error ok.
        # this may or may not make sense.
        tic2 = time.time()
        #Update mirror machines with PSLF values from power flow solution
        for gen in mirror.Machines:
            gen.getPvals()
        toc2 = time.time()
        mirror.IPYPvalsTime += toc2-tic2
        """

        #update mirror timers
        mirror.IPYdistPaccTime += toc1-tic1
        #mirror.IPYPvalsTime += toc2-tic2

        # Calculate global slack error (could be an average in the future?)
        mirror.globalSlack.getPvals()
        error = mirror.globalSlack.Pe_calc - mirror.globalSlack.Pe 
        
        if mirror.debug:
            print('expected: %.2f\tactual: %.2f\terror: %.2f' 
                  % (mirror.globalSlack.Pe_calc, mirror.globalSlack.Pe, error))

        # exit while loop if tolerance met
        if abs(error) <= tol:
            mirror.globalSlack.Pe_error = error
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
