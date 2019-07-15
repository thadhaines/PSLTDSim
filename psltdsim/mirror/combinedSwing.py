def combinedSwing(mirror, Pacc):
    """Calculates fdot, integrates to find next f, calculates deltaF. 
    Pacc in MW*sec, f and fdot are PU
    Currently Ignores system damping
    """
    
    # Handle frequency effect option
    if mirror.simParams['freqEffects'] == 1:
        f = mirror.cv['f']
    else:
        f = 1.0

    PaccPU = Pacc/mirror.Sbase
    HsysPU = mirror.Hsys/mirror.Sbase
    deltaF = 1.0-mirror.cv['f'] # this calc may be extra... unchanged since last ts

    # Swing equation
    fdot = 1/(2*HsysPU)*(PaccPU/f - mirror.Dsys*deltaF)
    mirror.cv['fdot'] = fdot

    # Adams Bashforth
    if mirror.simParams['integrationMethod'] == 'AB':
        mirror.cv['f'] = f + 1.5*mirror.timeStep*fdot  -0.5*mirror.timeStep*mirror.r_fdot[mirror.cv['dp']-1]

    elif mirror.simParams['integrationMethod'] == 'rk45':
        # use scipy int.
        tic = time.time()
        c = [HsysPU, PaccPU, mirror.Dsys, f]
        func = lambda t, y,c: 1/(2*c[0])*(c[1]/y - c[2]*(1-c[3]))
        w = solve_ivp(lambda t,y: func(t, y, c),
                      [0, mirror.timeStep], [f])
        mirror.cv['f'] = float(w.y[-1][-1]) # set current freq to last value
        mirror.IVPTime += time.time()-tic

    else:
        # Euler Integration - chosen by default
        mirror.cv['f'] = mirror.cv['f'] + (mirror.timeStep*fdot)
        # TODO: add statespace model of swing?

    # for logging
    # NOTE: changed 6/5/19 to more useful 1-f
    deltaF = 1.0 - mirror.cv['f'] #- mirror.r_f[mirror.cv['dp'] -1]
    mirror.cv['deltaF'] = deltaF