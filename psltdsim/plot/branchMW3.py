def branchMW3(mirror, FromBus1 , ToBusList1, FromBus2, ToBusList2, blkFlag=True, printFigs=False):
    """Plot total MW flow on line FromBusX -> ToBusListX where X = 1 or 2
    Uses External Bus Numbers
    Handles multiple to bus from a single 'from' bus - Twice!
    Used to calculate total South flow on COI (miniWECC bus 89)
    """
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
    mwFlow = np.zeros_like(mir.Branch[0].r_Pbr)
    initVal = np.ones_like(mir.Branch[0].r_Pbr)

    fig, ax = plt.subplots()
    for branch in mir.Branch:
        if (branch.Bus.Extnum == FromBus1) and (branch.TBus.Extnum in ToBusList1):
            mwFlow += branch.r_Pbr
        if (branch.Bus.Extnum == FromBus2) and (branch.TBus.Extnum in ToBusList2):
            mwFlow += branch.r_Pbr

    ax.plot(mins, initVal*mwFlow[0], linestyle = '-',linewidth=.8, c=[.7, .7, .7] )
    ax.plot(mins, mwFlow, linestyle = '-',linewidth=1,  )
    #ax.legend(loc='lower right', )

    toBusName1 = str(ToBusList1).replace('[','')
    toBusName1 = toBusName1.replace(']','')

    toBusName2 = str(ToBusList2).replace('[','')
    toBusName2 = toBusName2.replace(']','')

    ax.set_title(r'MW Branch Flow From '+str(FromBus1)+' to ' + toBusName1 +
                 ' and From '+str(FromBus2)+' to ' + toBusName2
                 +' \n Case: ' + caseName)

    ax.set_xlim(0,minEnd)
    ax.set_ylabel('Power Flow [MW]')
    ax.set_xlabel('Time [minutes]')
    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'BranchMWflow'+str(FromBus1)+'and' + str(FromBus2)+'.pdf', dpi=300)
    plt.show(block=blkFlag)
    plt.pause(0.00001) # required for true non-blocking print...