def combinedSwing(mirror, Pacc):
    """Calculates fdot, integrates to find next f, calculates deltaF. 
    Pacc in MW*sec, f and fdot are PU
    Currently Ignores system damping
    """
    
    # Handle frequency effect option
    if mirror.simParams['freqEffects'] == 1:
        f = mirror.c_f
    else:
        f = 1

    PaccPU = Pacc/mirror.Sbase
    HsysPU = mirror.Hsys/mirror.Sbase

    #ignore system damping for now
    # NOTE: Unsure how to calculate deltaF is it requires fdot -> Statespace
    Dsys = 0
    deltaF = 0

    # Swing equation
    fdot = 1/(2*HsysPU)*(PaccPU/f - Dsys*deltaF)
    mirror.c_fdot = fdot

    # Adams Bashforth
    if mirror.simParams['integrationMethod'] == 'AB':
        mirror.c_f = mirror.c_f + 1.5*mirror.timeStep*fdot  -0.5*mirror.timeStep*mirror.r_fdot[mirror.c_dp-1]
    elif mirror.simParams['integrationMethod'] == 'rk45':
        # use scipy int...
        mirror.c_f = mirror.c_f + (mirror.timeStep*fdot)
    else:
        # Euler Integration - chosen by default
        # matches PSLF better than the adams bashforth method in ee554 load case
        mirror.c_f = mirror.c_f + (mirror.timeStep*fdot)

    # for logging
    deltaF = mirror.c_f - mirror.r_f[mirror.c_dp -1]
    mirror.c_deltaF = deltaF