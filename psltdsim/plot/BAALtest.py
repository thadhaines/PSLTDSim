def BAALtest(mirror, blkFlag=True, printFigs=False):
    """Meant to test adherence to BA ACE Limits."""
    # simple visual test as of 12/30/19

    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror
    xend = max(mir.r_t)
    mini = 1 # can be increased to scale width of plots

    caseName = mir.simParams['fileName'][:-1]

    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    firstPlot = True
    # Create single clock minute Average Frequency...
    fig, ax = plt.subplots()

    ax.plot(mins, mir.r_f)

    # Create list of clock minute average frequency
    ts = mir.simParams['timeStep']
    Nsmp = int(60/ts) # number of samples per minute
    sNDX = 0
    done = False
    aveF = np.zeros_like(mir.r_f)

    while not done:
        eNDX = sNDX + Nsmp
        if eNDX > len(mir.r_f)-1:
            eNDX = len(mir.r_f)-1
            done = True
            preVal = sumF/Nsmp

        sumF = sum(mir.r_f[sNDX:eNDX])
        aveF[sNDX:eNDX] = sumF/Nsmp
        
        sNDX = eNDX
        if done:
            aveF[eNDX:] = preVal

    ax.plot(mins, aveF)
    plt.show(block=False)


    for BA in mir.BA:
        # Create seperate figure for each BA
        fig, ax = plt.subplots()

        # calcs for BAAL
        eps = 0.0228 # ave Hz
        BAAL = []
        fBase = mir.simParams['fBase']

        for fa in aveF:

            if fa < 1:
                FTL = fBase-3*eps
            else:
                FTL = fBase+3*eps
            #not the best way to do this
            BAAL.append(-10*BA.B*(FTL-fBase) * (FTL-fBase)/(fa*fBase-fBase))

        ax.plot(mins,BA.r_RACE,
                label ='RACE')
        ax.plot(mins,BAAL,
                label = 'BAAL')
        
        if firstPlot:
            # Scale current axis.
            box = ax.get_position()
            boxW = box.width * 1.05
            firstPlot = False

        ax.set_position([box.x0, box.y0, boxW, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_title(r'Area '+str(BA.Area.Area)+' ('+ BA.name + ') BAAL \n Case: ' + caseName)
        ax.set_xlim(0,minEnd)
        ax.set_ylabel('y axis')
        ax.set_xlabel('Time [minutes]')

        #ax.legend(loc=0)
        ax.grid(True)
        fig.set_dpi(150)
        fig.set_size_inches(9/mini, 2.5)
        fig.tight_layout()
        plt.show(block=False)
        if printFigs: plt.savefig(caseName+BA.name+'BAAL.pdf', dpi=300)
        plt.pause(0.00001) # required for true non-blocking print...


    plt.show(block = blkFlag)
    plt.pause(0.00001)