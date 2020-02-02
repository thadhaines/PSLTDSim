def sysBranchMVAR(mirror, blkFlag=True, printFigs=False):
    """Plot MVAR flow per branch """
    
    import matplotlib.pyplot as plt
    from matplotlib.offsetbox import AnchoredText # for text box
    import numpy as np

    mir = mirror

    ### Plot Valve Travel, total in legend
    xend = max(mir.r_t)
    caseName = mir.simParams['fileName'][:-1]
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    mini = 1


    fig, ax = plt.subplots()
    govMachines = 0 # for average movement
    aveTravel = 0

    for branch in mir.Branch:

        ax.plot(mins, branch.r_Qbr, linestyle = '-',linewidth=1,
                label = 'Branch ' + str(branch.Bus.Extnum) +' to ' +str(branch.TBus.Extnum))
        
    if govMachines > 0:
        # Annotate average valve movement
        stringToPrint = "Average Area Travel "+str(round(aveTravel/govMachines,2))
        anchoredText = AnchoredText(stringToPrint, loc='upper right')
        ax.add_artist(anchoredText)


    ax.legend(loc='lower right', )

    ax.set_title('MVAR Flow\n Case: ' + caseName)
    ax.set_xlim(0,minEnd)
    ax.set_ylabel('Flow [MVAR]')
    ax.set_xlabel('Time [minutes]')
    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    plt.show(block=blkFlag)
    if printFigs: plt.savefig(caseName+'sysBranchMVAR'+'.pdf', dpi=300)
    plt.pause(0.00001) # required for true non-blocking print...