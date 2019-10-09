def oneGenDynamics(mirror, blkFlag=True, printFigs = False, genNum = 0):
    """Plot all dynamic responses from generators
    does not block by default - blkFlag ignored
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import psltdsim as ltd

    mir = mirror

    # Handle bad input
    cGen = ltd.find.findGenOnBus(mir, genNum, None, False)
    if cGen == None:
        print("No generator found on bus %d." % genNum)
        return

    if cGen.gov_model == False:
        print("Generator on bus %d has no governor." % genNum)
        return

    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)

    # plot generator dynamic data
    fig, ax = plt.subplots(nrows=2, ncols=1,)
    ax[0].set_title('Governed Generator on Bus %d %s Power Output' 
                    % (cGen.Busnum, cGen.Busnam,))
    ax[1].set_title('Governor States')

    ax[0].plot(mins, cGen.r_Pm, 
                #marker = '+',
                #linestyle = '--',
                label = 'Pm')
    ax[0].plot(mins, cGen.r_Pe, 
                #marker = 'o',
                #markerfill = 'None',
                linestyle = '--',
                label = 'Pe')

    ax[1].plot(mins, cGen.gov_model.r_x1, 
                #marker = '1',
                #linestyle = '--',
                label = 'x1')
    ax[1].plot(mins, cGen.gov_model.r_x2, 
                #marker = '2',
                linestyle = '--',
                label = 'x2')

    ax[0].set_xlabel('Time [minutes]')
    ax[1].set_xlabel('Time [minutes]')
    ax[0].set_ylabel('MW')
    ax[1].set_ylabel('State')
    # Global Plot settings
    for x in np.ndarray.flatten(ax):
        x.set_xlim(0,minEnd)
        x.legend()
        x.grid(True)

    fig.tight_layout()

    plt.show(block = blkFlag)
    plt.pause(0.00001)