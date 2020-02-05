def sysH(mirror, blkFlag=True, printFigs=False):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror
    xend = max(mir.r_t)
    mini = 1 # can be increased to scale width of plots

    caseName = mir.simParams['fileName'][:-1]
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)

    ## Plot System Frequency

    fig, ax = plt.subplots()

    ax.plot(mins, mir.r_Hsys, linewidth=1)


    ax.set_title('System Inertia\n Case: ' + caseName)
    ax.set_ylabel('Inertia [MW s]')
    ax.set_xlabel('Time [minutes]')
    ax.set_xlim(0,minEnd)
    #ax.legend()
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'sysH'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)