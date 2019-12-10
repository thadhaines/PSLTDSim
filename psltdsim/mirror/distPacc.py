def distPacc(mirror, deltaPacc):
    """Distribute Pe among generators until global slack error below tolerance.

    Assumes:
        Each system has only 1 global slack bus
        Each area has it's own designated slack gen (though it may not be used)

    NOTE: pretty rough on the mulitple slack generator handling (i.e. untested) - might work if in seperate islands....
    TODO: IRP_flag..., and mw limits of generators (Pmax)

    Same as original disPacc,with removal of slack inertia before second pass and
    all mirror agents refreshed each solution attempt
    """

    tol_Flag = 1 # goes to zero once error < tolerance

    tol = mirror.slackTol
    error = tol + 1
    Hss = mirror.ss_H # MW*sec
    Pacc = deltaPacc
    iteration = 1

    while tol_Flag:
        tic1 = time.time()
        if mirror.debug:
            print("*** LTD: Distributing %.2f MW of Pacc, Iteration %d" % (Pacc, iteration))
        #for each system area:
        for c_gen in mirror.Machines:

            # Ensure off generators don't suppy power or get Pacc distribution
            if c_gen.cv['St'] == 0:
                #c_gen.cv['Pe'] = 0
                #c_gen.cv['Q'] = 0
                #c_gen.setPvals()
                continue

            # Assume gens with default Pe = 0.0 do not supply real power
            #if c_gen.cv['Pe'] == 0.0:
            #    continue

            if c_gen.globalSlack:
                if iteration == 1:
                    #distribute to slack on First pass 
                    c_gen.cv['Pe'] = c_gen.cv['Pe'] - Pacc * (c_gen.H/Hss)
                    # Set Pe_calc
                    c_gen.cv['Pe_calc'] = c_gen.cv['Pe'] 
                    globalSlackH = c_gen.H
                else:
                    # On later iterations, Reset generator to estimated value
                    c_gen.cv['Pe'] = c_gen.cv['Pe_calc']
            
                # Update PSLF values
                c_gen.setPvals()
                c_gen.Bus.setPvals()
                

            #Distribute delta Pacc to non slack other gens
            else:
                c_gen.cv['Pe'] = c_gen.cv['Pe'] - Pacc * (c_gen.H/Hss) 
                c_gen.setPvals()
                c_gen.Bus.setPvals()

            #if mirror.debug:
                    #print("*** Set %s Pe to %.2f" % (c_gen, c_gen.cv['Pe']))
                    #print("*** Set %s V to %.2f" % (c_gen.Bus, c_gen.Bus.cv['Vm']))

        toc1 = time.time()
        # Pe is distributed to all generators in all areas, solve Power flow
        ltd.mirror.LTD_SolveCase(mirror)

        #update mirror timers
        mirror.IPYdistPaccTime += toc1-tic1

        # Calculate global slack error (could be an average in the future?)
        mirror.globalSlack.getPvals()
        error = mirror.globalSlack.cv['Pe_calc'] - mirror.globalSlack.cv['Pe'] 
        
        if mirror.debug:
            print('expected: %.2f\tactual: %.2f\terror: %.2f' 
                  % (mirror.globalSlack.cv['Pe_calc'], mirror.globalSlack.cv['Pe'], error))

        tic2 = time.time()
        #Update mirror machines with PSLF values from power flow solution
        for gen in mirror.Machines:
            gen.getPvals()
        toc2 = time.time()
        mirror.IPYPvalsTime += toc2-tic2

        # exit while loop if tolerance met
        if abs(error) <= tol:
            mirror.globalSlack.cv['Pe_error'] = error
            # Upldate flow calcd table.... Doesn't seem to do the desired thing 10/14
            #calcFlows = "flowcalcd(1)"
            #PSLF.RunEpcl(calcFlows)
            tol_Flag = 0
            continue

        # tolerance not met, redistribute error to all machines minus global slack
        if iteration == 1:
            # Only remove global inertia once
            Hss -= globalSlackH

        Pacc = error
        iteration +=1

        if iteration > 20:
            '''Solution did not converge'''
            raise ValueError('*** PSLF power flow solution exceeded Max iterations... 20')
            return

