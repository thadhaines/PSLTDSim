def combinedSwing(model, Pacc, freqFlag=0):
    """Calculates fdot, integrates to find next f, calculates deltaF. 
    Pacc in MW*sec, f and fdot are PU
    FreqFlag optional - set to 1 to ignore frequency effects in swing equation
    Currently Ignores system damping
    """
    
    # Handle frequency effect option
    if freqFlag != 1:
        f = model.c_f
    else:
        f = 1

    PaccPU = Pacc/model.Sbase
    HsysPU = model.Hsys/model.Sbase

    #ignore system damping for now
    # NOTE: Unsure how to calculate deltaF is it requires fdot -> Statespace
    Dsys = 0
    deltaF = 0

    # Swing equation
    fdot = 1/(2*HsysPU)*(PaccPU/f - Dsys*deltaF)
    model.c_fdot = fdot

    # Euler Integration 
    # matches PSLF better than the adams bashforth method in ee554 load case
    model.c_f = model.c_f + (model.timeStep*fdot)

    # Adams Bashforth
    #model.c_f = model.c_f + (model.timeStep*fdot)*(1.5*model.r_f[model.c_dp-1] -0.5*model.r_f[model.c_dp-2])

    # for logging
    deltaF = model.c_f - model.r_f[model.c_dp -1]
    model.c_deltaF = deltaF