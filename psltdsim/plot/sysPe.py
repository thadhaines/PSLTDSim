def sysPe(mirror, blkFlag=True, printFigs=False):
    """Plot Pe from all gens in a given mirror
    Uses cycler for colors - repeats after 6
    """
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