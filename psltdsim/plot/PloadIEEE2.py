def PloadIEEE2(mirror, blkFlag=True, printFigs=False, miniFlag = False):
    """Plot load changes for system and each area"""
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

    ax.plot(mins, np.array(mir.r_ss_Pload)-mir.r_ss_Pload[0], linewidth=1.0, 
            #color='black',
            label = 'System Total')

    for area in mir.Area:
        ax.plot(mins, np.array(area.r_P)-area.r_P[0], 
                linewidth=.85,
                linestyle="--",
                label = 'Area '+ str(area.Area)
                )

    # Scale current axis.
    box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 1.05, box.height])

    # Put a legend to the right of the current axis
    #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    ax.set_title('Change in System Loading')
    ax.set_xlim(0,minEnd)
    ax.set_ylabel('MW')
    ax.set_xlabel('Time [minutes]')
    ax.legend()

    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    #fig.set_size_inches(9/lengDiv, 2.5*.75)
    fig.set_size_inches(9, 2.5) # single column, double height for legend below

    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'PloadChange'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)