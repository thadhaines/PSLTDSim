def sysF(mirror, blkFlag=True, printFigs=False):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror
    xend = max(mir.r_t)
    mini = 1 # can be increased to scale width of plots

    caseName = mir.simParams['fileName'][:-1]
    # Plot controlled machines Pref and Pm
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)

    ## Plot System Frequency
    # find smallest BA dead band
    deadbands = ['step', 'ramp', 'nldroop']
    dbLine = 1
    plotDb= False
    for BA in mir.BA:
        if BA.BAdict['GovDeadbandType'].lower() in deadbands:
            cDBline = BA.BAdict['GovDeadband']
            if BA.BAdict['GovDeadbandType'].lower() == 'nldroop':
                cDBline = BA.BAdict['GovAlpha']

            if cDBline < dbLine:
                dbLine = cDBline
                plotDb= True

    fig, ax = plt.subplots()
    fig.set_size_inches(6, 2)
    ax.plot(mins, np.array(mir.r_f)*60.0,linewidth=1, label = 'Frequency')

    if plotDb:
        highDb = np.ones_like(mir.r_f)*mir.fBase+dbLine
        lowDb = np.ones_like(mir.r_f)*mir.fBase-dbLine
        ax.plot(mins, highDb,linewidth=1,linestyle=":",C='0.3')
        ax.plot(mins,lowDb,linewidth=1,linestyle=":",C='0.3', label = str(dbLine)+' Hz Governor Deadband')
        ax.legend(loc='center right')

    ax.set_title('System Frequency\n Case: ' + caseName)
    ax.set_ylabel('Hz')
    ax.set_xlabel('Time [minutes]')
    ax.set_xlim(0,minEnd)
    #ax.legend()
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'Freq'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)