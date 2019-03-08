def LTD_SolveCase(mirror):
    """Solves power flow using custom solve parameters
    Returns PSLF errorCode if available
    Only option not default is area interchange adjustment (turned off)
    """
    #global PSLF
    
    errorCode = PSLF.SolveCase(
        25, # maxIterations, Solpar.Itnrmx
        0, 	# iterationsBeforeVarLimits, Solpar.Itnrvl
        0,	# flatStart, 
        1,	# tapAdjustment, Solpar.Tapadj
        1,	# switchedShuntAdjustment, Solpar.Swsadj
        1,	# phaseShifterAdjustment, Solpar.Psadj
        0,	# gcdAdjustment, probably Solpar.GcdFlag
        0,	# areaInterchangeAdjustment, 
        1,	# solnType, 1 == full, 2 == DC, 3 == decoupled 
        0,  # reorder (in dypar default = 0)
        )
    
    if mirror.debug: print('Power Flow Solution returns: %d' % errorCode)

    if errorCode == -1:
        '''Solution did not converge'''
        raise ValueError('PSLF power flow solution did not converge.')
        return