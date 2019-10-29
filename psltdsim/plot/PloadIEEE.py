def PloadIEEE(mirror, blkFlag=True, printFigs=False, miniFlag = False):
    """Plot SACE of given mirror areas"""
    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror

    # for 2 column presentation
    if miniFlag:
        lengDiv = 2
    else:
        lengDiv = 1

    ### Plot detailed SACE
    #Plot SACE from all areas on same plot
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    caseName = mir.simParams['fileName'][:-1]

    fig, ax = plt.subplots()

    ax.plot(mins, mir.r_ss_Pload, linewidth=1.25,)

    # Scale current axis.
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1.05, box.height])

    # Put a legend to the right of the current axis
    #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    ax.set_title('System Loading')
    ax.set_xlim(0,minEnd)
    ax.set_ylabel('MW')
    ax.set_xlabel('Time [minutes]')

    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/lengDiv, 4.5*.65)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'Pload'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)