def combinedSwing(model, Pacc, freqFlag=1):
    """Calculates fdot and integrates to find next f. Pacc in MW*sec
    FreqFlag optional - bypass frequency effects - set to 0 to account for
    Currently Ignores system damping

    NOTE: not verified! - it does stuff, but maybe not correctly.... feels 1 step too fast
    """
    
    # Handle frequency effect optoins
    if freqFlag != 1:
        f = model.c_f
    else:
        f = 1

    PaccPU = Pacc/model.Sbase
    HsysPU = model.Hsys/model.Sbase

    #ignore system damping for now, unsure how to calculate deltaF at this point, requires fdot
    Dsys = 0
    deltaF = 0

    # Swing equation
    fdot = 1/(2*HsysPU)*(PaccPU/f - Dsys*deltaF)
    model.c_fdot = fdot

    # lazy integration
    model.c_f = model.c_f + (model.timeStep*fdot)

    deltaF = model.c_f - model.r_f[model.c_dp -1]
    model.c_deltaF = deltaF