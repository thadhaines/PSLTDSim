def BAplots02(mirror, blkFlag=True, printFigs=False):
    """Same as BAplots01, except internal legends"""
    import matplotlib.pyplot as plt
    import numpy as np

    # custom color cycler
    from cycler import cycler
    ltdColors=[ [0,0,0], # black
            [.7,.7,.7], # grey
            [0,1,0], # green
            [1,0,1], # magenta
            "#17becf", # light blue
            [1,.647,0],# orange
        ]
    default_cycler = (cycler(color=ltdColors))
    plt.rc('axes', prop_cycle=default_cycler)

    mir = mirror
    xend = max(mir.r_t)
    mini = 1 # can be increased to scale width of plots

    caseName = mir.simParams['fileName'][:-1]
    # Plot controlled machines Pref and Pm
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)

    for BA in mir.BA:
        fig, ax = plt.subplots()
        for gen in BA.ctrlMachines:
            normVal = gen.r_Pm[0]
            ax.plot(mins, np.array(gen.r_Pm)/normVal, linestyle = '-',linewidth=1,
                    label = r'$P_m$  '+str(gen.Busnum)+' '+gen.Id+' Norm: '+str(round(normVal))  )
            ax.plot(mins, np.array(gen.r_Pref)/normVal, linestyle = '--',linewidth=1.5,
                    label = r'$P_{ref}$ '+str(gen.Busnum)+' '+gen.Id  )
        

        # Put a legend to the right of the current axis
        ax.legend(loc='lower right')

        ax.set_title(r'Area '+str(gen.Area)+' ('+ BA.name + ') Controlled Machines $P_m$ and $P_{ref}$ \n Case: ' + caseName)
        ax.set_xlim(0,minEnd)
        ax.set_ylabel('Normalized % Change [MW]')
        ax.set_xlabel('Time [minutes]')
        #ax.legend(loc=0)
        ax.grid(True)
        fig.set_dpi(150)
        fig.set_size_inches(9/mini, 2.5)
        fig.tight_layout()
        plt.show(block=False)
        if printFigs: plt.savefig(caseName+BA.name+'.pdf', dpi=300)
        plt.pause(0.00001) # required for true non-blocking print...

    #Plot Interchange Error and ACE on same plot
    fig, ax = plt.subplots()
    for BA in mir.BA:
        ax.plot(mins, BA.r_RACE, linewidth=1,
                label= BA.name+' RACE')
        if BA.filter != None:
            ax.plot(mins, BA.r_ACE2dist, linewidth=1.25,linestyle=":",
                    label= BA.name+' DACE')
        ax.plot(mins, BA.Area.r_ICerror, linewidth=1.5,
                linestyle='--',
                label= BA.name +' IC Error')

    # Put a legend to the right of the current axis
    ax.legend(loc='lower right')

    ax.set_title('Balancing Authority ACE and Interchange Error\n Case: ' + caseName)
    ax.set_xlim(0,minEnd)
    ax.set_ylabel('MW')
    ax.set_xlabel('Time [minutes]')

    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    plt.show(block=False)
    if printFigs: plt.savefig(caseName+'RACE'+'.pdf', dpi=300)
    plt.pause(0.00001)

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

    ax.set_title('System Frequency\n Case: ' + caseName)
    ax.set_ylabel('Hz')
    ax.set_xlabel('Time [minutes]')
    ax.set_xlim(0,minEnd)
    # Put a legend to the right of the current axis
    ax.legend(loc='lower right')
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'Freq'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)