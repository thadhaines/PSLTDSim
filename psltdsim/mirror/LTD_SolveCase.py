def LTD_SolveCase(mirror=None):
    """Solves power flow using custom solve parameters
    Returns PSLF errorCode if available
    Only option not default is area interchange adjustment (turned off)
    """
    if mirror == None:
        flatStart = 0
    else:
        flatStart = 0 # never flat start ( could be changed to solnType options ) or reorder?
        if mirror.debug: print('flat start = %d' % flatStart)

    soln_start = time.time()
    errorCode = PSLF.SolveCase(
        25, # maxIterations, Solpar.Itnrmx
        0, 	# iterationsBeforeVarLimits, Solpar.Itnrvl
        0,	# flatStart, 
        1,	# tapAdjustment, Solpar.Tapadj 1
        1,	# switchedShuntAdjustment, Solpar.Swsadj 1
        1,	# phaseShifterAdjustment, Solpar.Psadj 1
        0,	# gcdAdjustment, probably Solpar.GcdFlag 0
        0,	# areaInterchangeAdjustment, 
        1,	# solnType, 1 == full, 2 == DC, 3 == decoupled 
        0,  # reorder (in dypar default = 0)
        )
    soln_end = time.time()

    #handle timing 
    if mirror:
        mirror.PFTime += (soln_end - soln_start)
        mirror.PFSolns += 1
        if mirror.debug: print('Power Flow Solution returns: %d' % errorCode)

    if errorCode == -1:
        '''Solution did not converge'''
        raise ValueError('*** PSLF power-flow solution did not converge.')
        return
    if errorCode == -2:
        '''Maximum iterations hit'''
        raise ValueError('*** PSLF power-flow solution stopped due to maximum number of iterations.')
        return

    #converged
    return