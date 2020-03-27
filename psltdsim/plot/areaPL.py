def areaPL(mirror, blkFlag=True, printFigs=False):
    """Plot area Powergen and Load"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    mir = mirror
    caseName = mir.simParams['fileName'][:-1]
    mins = np.array(mir.r_t)/60.0;
    xend = max(mins)
    mini = 1

    fig, ax = plt.subplots()

    ax.set_title('Area Generation and Demand\n Case: ' + caseName)

    for area in mir.Area:
        ax.plot(mins, area.r_Pe, 
                    linewidth = 2,
                    label = r'$P_e$ Area '+ str(area.Area)
                    )
        ax.plot(mins, area.r_P, 
                    linewidth = 2,
                    linestyle = '--',
                    label = r'$P$ Area '+ str(area.Area)
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
    if printFigs: plt.savefig(caseName+'areaPL'+'.pdf', dpi=300)
    plt.pause(0.00001) # required for true non-blocking print...