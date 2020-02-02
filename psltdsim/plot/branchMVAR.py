def branchMVAR(mirror, FromBus , ToBusList, blkFlag=True, printFigs=False):
    """Plot total MVAR flow on line FromBus -> ToBusList
    Uses External Bus Numbers
    Handles multiple to bus from a single 'from' bus
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
    mwFlow = np.zeros_like(mir.Branch[0].r_Qbr)
    initVal = np.ones_like(mir.Branch[0].r_Qbr)

    fig, ax = plt.subplots()
    for branch in mir.Branch:
        if (branch.Bus.Extnum == FromBus) and (branch.TBus.Extnum in ToBusList):
            mwFlow += branch.r_Qbr

    for xmfr in mir.XFMR:
        if (xmfr.Bus.Extnum == FromBus) and (xmfr.TBus.Extnum in ToBusList):
            mwFlow += xmfr.r_Qbr

    ax.plot(mins, initVal*mwFlow[0], linestyle = '-',linewidth=.8, c=[.7, .7, .7] )
    ax.plot(mins, mwFlow, linestyle = '-',linewidth=1,  )
    #ax.legend(loc='lower right', )

    toBusName = str(ToBusList).replace('[','')
    toBusName = toBusName.replace(']','')

    ax.set_title(r'MVAR Flow From Bus '+str(FromBus)+' to ' + toBusName
                 +' \n Case: ' + caseName)

    ax.set_xlim(0,minEnd)
    ax.set_ylabel('Power Flow [MVAR]')
    ax.set_xlabel('Time [minutes]')
    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    toBusName = toBusName.replace(',','-')
    if printFigs: plt.savefig(caseName+'MVarflow'+str(FromBus)+'to' + toBusName.replace(' ','')+'.pdf', dpi=300)
    plt.show(block=blkFlag)
    plt.pause(0.00001) # required for true non-blocking print...