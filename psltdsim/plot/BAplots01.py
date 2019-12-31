def BAplots01(mirror, blkFlag=True, printFigs=False):
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
    firstPlot = True

    for BA in mir.BA:
        fig, ax = plt.subplots()
        for gen in BA.ctrlMachines:
            normVal = gen.r_Pm[0]
            ax.plot(mins, np.array(gen.r_Pm)/normVal, linestyle = '-',linewidth=1,
                    label = r'$P_m$  '+str(gen.Busnum)+' '+gen.Id+' Norm: '+str(round(normVal))  )
            ax.plot(mins, np.array(gen.r_Pref)/normVal, linestyle = '--',linewidth=1.5,
                    label = r'$P_{ref}$ '+str(gen.Busnum)+' '+gen.Id  )
        
        if firstPlot:
            # Scale current axis.
            box = ax.get_position()
            boxW = box.width * 1.05
            firstPlot = False

        ax.set_position([box.x0, box.y0, boxW, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

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
            ax.plot(mins, BA.r_SACE, linewidth=1.25,linestyle=":",
                    label= BA.name+' SACE')
        ax.plot(mins, BA.Area.r_ICerror, linewidth=1.5,
                linestyle='--',
                label= BA.name +' IC Error')
    # Scale current axis.
    #box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1.05, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

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
    ax.legend()
    #ax.legend()
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'Freq'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)