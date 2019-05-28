def combinedSwing(mirror, Pacc):
    """Calculates fdot, integrates to find next f, calculates deltaF. 
    Pacc in MW*sec, f and fdot are PU
    Currently Ignores system damping
    """
    
    # Handle frequency effect option
    if mirror.simParams['freqEffects'] == 1:
        f = mirror.c_f
    else:
        f = 1.0

    PaccPU = Pacc/mirror.Sbase
    HsysPU = mirror.Hsys/mirror.Sbase
    deltaF = 1-mirror.c_f

    # Swing equation
    fdot = 1/(2*HsysPU)*(PaccPU/f - mirror.Dsys*deltaF)
    mirror.c_fdot = fdot

    # Adams Bashforth
    if mirror.simParams['integrationMethod'] == 'AB':
        mirror.c_f = mirror.c_f + 1.5*mirror.timeStep*fdot  -0.5*mirror.timeStep*mirror.r_fdot[mirror.c_dp-1]
    elif mirror.simParams['integrationMethod'] == 'rk45':
        # use scipy int.
        tic = time.time()
        c = [HsysPU, PaccPU, mirror.Dsys, mirror.c_f]
        f = lambda t, y,c: 1/(2*c[0])*(c[1]/y - c[2]*(1-c[3]))
        w = solve_ivp(lambda t,y: f(t, y, c),
                      [0, mirror.timeStep], [mirror.c_f])
        mirror.c_f = float(w.y[-1][-1]) # set current freq to last value
        mirror.IVPTime += time.time()-tic
    else:
        # Euler Integration - chosen by default
        mirror.c_f = mirror.c_f + (mirror.timeStep*fdot)

    # for logging
    deltaF = mirror.c_f - mirror.r_f[mirror.c_dp -1]
    mirror.c_deltaF = deltaF