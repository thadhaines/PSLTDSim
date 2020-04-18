def BAALtest(mirror, blkFlag=True, printFigs=False):
    """Meant to test adherence to BA ACE Limits."""
    # simple visual test as of 12/30/19

    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    mir = mirror
    xend = max(mir.r_t)
    mini = 1 # can be increased to scale width of plots

    caseName = mir.simParams['fileName'][:-1]

    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    #firstPlot = True
    # Create single clock minute Average Frequency...
    fig, ax = plt.subplots()

    ax.plot(mins, np.array(mir.r_f)*mir.fBase , label='Frequency', c=[0,0,0],
            linewidth=1.0)

    ## Create list of clock minute average frequency
    ts = mir.simParams['timeStep']
    Nsmp = int(60/ts) # number of samples per minute
    aveF = np.zeros_like(mir.r_f)

    sNDX = 0
    done = False
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

    ax.plot(mins, np.array(aveF)*mir.fBase, label="Minute Average",color=[1,0,1]
            , alpha=0.66)
    ax.set_title('Minute Average System Frequency \n Case: ' + caseName)
    ax.set_xlim(0,minEnd)
    ax.set_ylabel('Frequency [Hz]')
    ax.set_xlabel('Time [minutes]')

    ax.grid(True)
    ax.legend(loc='right')
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    plt.show(block=False)
    if printFigs: plt.savefig(caseName+'MinFave.pdf', dpi=300)
    plt.pause(0.00001) # required for true non-blocking print...


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
            # negative from B removed as this is typicall a neg val
            BAAL.append(10*BA.B*(FTL-fBase) * (FTL-fBase)/(fa*fBase-fBase))

        ax.plot(mins,BA.r_RACE,
                linewidth=1.0,
                c=[0,0,0],
                label ='RACE')
        #ax.plot(mins,BAAL,
                #c=[0,1,0],
                #label = 'BAAL')
        ax.fill_between(mins, 0, BAAL,
                        color=[0,1,0],
                        #alpha=0.75,
                label = 'BAAL')

        overBAAL = []
        for (baal, race) in itertools.zip_longest(BAAL, BA.r_RACE):


            if baal > 0 and race > baal:
                # violation
                overBAAL.append(1)
                continue

            if baal < 0 and race < baal:
                # violation
                overBAAL.append(-1)
                continue

            overBAAL.append(0)

        #ax.plot(mins,np.array(overBAAL)*max(BAAL),
                #c=[1,0,1],
                #label = 'OverBAAL')
        ax.fill_between(mins, 0, np.array(overBAAL)*max(np.abs(BAAL)),
                        color=[1,0,1],
                        alpha=0.666,
                label = 'BAAL Exceeded')
        
        #if firstPlot:
            # Scale current axis.
            #box = ax.get_position()
            #boxW = box.width * 1.05
            #firstPlot = False

        #ax.set_position([box.x0, box.y0, boxW, box.height])

        # Put a legend to the right of the current axis
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        #print(overBAAL)# DEBUG

        ax.legend(loc='right')
        ax.set_title(r'Area '+str(BA.Area.Area)+' ('+ BA.name + ') BAAL \n Case: ' + caseName)
        ax.set_xlim(0,minEnd)

        # scale obsurd axis
        if max(BAAL)/50 > max(BA.r_RACE):
            ax.set_ylim(min(BA.r_RACE)*1.25, max(BA.r_RACE)*1.25)

        ax.set_ylabel('ACE [MW]')
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