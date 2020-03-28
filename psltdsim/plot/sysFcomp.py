def sysFcomp(mirrorList, blkFlag=True, printFigs=False):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np
    import psltdsim as ltd

    plt.rcParams.update({'font.size': 9}) # used to scale text


    fig, ax = plt.subplots()
    fig.set_size_inches(6, 2)
    plotDb= False
    dbDict = {} # blank dictionary for collecting deadbands
    deadbands = ['step', 'ramp', 'nldroop']

    colors=[ [0,0,0],
            [.7,.7,.7],
            [0,1,0],
            [1,0,1],
            #[0,1,1], # cyan
            "#17becf", # light blue
            [1,.647,0],# orange
            #"#ff7f0e", #orange
        ]
    styles =["-","--",':','-.'
        ]
    sNDX = 0

    for mirror in mirrorList:
        mir = ltd.data.readMirror(mirror)
        xend = max(mir.r_t)
        mini = 1 # can be increased to scale width of plots

        caseName = mir.simParams['fileName'][:-1]
        # Plot controlled machines Pref and Pm
        mins = np.array(mir.r_t)/60.0;
        minEnd = max(mins)

        ## Plot System Frequencies
        for BA in mir.BA:

            dbTypeSTR ='None'
            if BA.BAdict['GovDeadbandType'].lower() in deadbands:
                cDBline = BA.BAdict['GovDeadband']

                if BA.BAdict['GovDeadbandType'].lower() == 'nldroop':
                    cDBline = BA.BAdict['GovAlpha']
                    dbTypeSTR ='Non-Linear'

                if BA.BAdict['GovDeadbandType'].lower() == 'step':
                    dbTypeSTR ='Step'

                if BA.BAdict['GovDeadbandType'].lower() == 'ramp':
                    dbTypeSTR ='No-Step'

                if abs(cDBline) > 0:
                    dbDict[str(cDBline)] = cDBline
                    plotDb= True
        # plot freq
        ax.plot(mins, np.array(mir.r_f)*60.0,linewidth=1,  
                        #linestyle=styles[sNDX],
                        color=colors[sNDX],
                        label = 'Deadband: '+ dbTypeSTR)
        sNDX+=1

    if plotDb:
        for foundDB in dbDict:
            dbLine = dbDict[str(foundDB)]
            highDb = np.ones_like(mir.r_f)*mir.fBase+dbLine
            lowDb = np.ones_like(mir.r_f)*mir.fBase-dbLine
            ax.plot(mins, highDb,linewidth=1,linestyle=":",C='0.3')
            ax.plot(mins,lowDb,linewidth=1,linestyle=":",C='0.3')#, label = str(dbLine)+' Hz Governor Deadband')

    ax.set_title('System Frequency')
    ax.set_ylabel('Hz')
    ax.set_xlabel('Time [minutes]')
    ax.set_xlim(0,minEnd)
    #ax.legend(loc='upper right')#, bbox_to_anchor=(0.5, -0.2))
    ax.legend()
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9, 2.5) # single column, double height for legend below
    #fig.set_size_inches(9/2, 2.5*.75) # single column, double height for legend below
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'Freq'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)