def combinedSwing(model, Pacc):
    """Calculates fdot, integrates to find next f, calculates deltaF. 
    Pacc in MW*sec, f and fdot are PU
    Currently Ignores system damping
    """
    
    # Handle frequency effect option
    if model.simParams['freqEffects'] == 1:
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

    # Adams Bashforth
    if model.simParams['integrationMethod'] == 'AB':
        model.c_f = model.c_f + (model.timeStep*fdot)*(1.5*model.r_f[model.c_dp-1] -0.5*model.r_f[model.c_dp-2])
    else:
        # Euler Integration - chosen by default
        # matches PSLF better than the adams bashforth method in ee554 load case
        model.c_f = model.c_f + (model.timeStep*fdot)

    # for logging
    deltaF = model.c_f - model.r_f[model.c_dp -1]
    model.c_deltaF = deltaF