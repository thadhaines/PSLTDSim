def sysPe(mirror, blkFlag=True, printFigs=False):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.cm import get_cmap

    name = "tab20"
    cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
    colors = cmap.colors  # type: list
    #print(colors)
    
    mir = mirror
    caseName = mir.simParams['fileName'][:-1]
    mins = np.array(mir.r_t)/60.0;
    xend = max(mins)
    mini = 1

    fig, ax = plt.subplots()

    ax.set_title('Generator Power Distriubtion\n Case: ' + caseName)
    for mach in mir.Machines:
        ax.plot(mins, mach.r_Pe, 
                    linewidth = 2,
                    label = r'$P_e$ Gen '+ mach.Busnam+' '+mach.Id
                    )

    ax.set_ylabel('MW')
    ax.set_xlabel('Time [minutes]')
    ax.legend(loc=1)
    ax.set_xlim(0,xend)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9, 2.5)
    fig.tight_layout()
    plt.show(block=blkFlag)
    if printFigs: plt.savefig(caseName+'sysPe'+'.pdf', dpi=300)
    plt.pause(0.00001) # required for true non-blocking print...