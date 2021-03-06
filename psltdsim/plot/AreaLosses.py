def AreaLosses(mirror, blkFlag=True, printFigs=False):
    """Plot AreaLosses of given mirror areas"""
    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror
    ### Plot Area Change in Losses over time
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    caseName = mir.simParams['fileName'][:-1]
    mini = 1

    fig, ax = plt.subplots()
    for area in mir.Area:
        ax.plot(mins, np.array(area.r_Losses)-area.r_Losses[0], linewidth=1.25,#linestyle=":",
                    label= 'Area '+ str(area.Area)+', Norm: '+ str(int(area.r_Losses[0])))

    # Scale current axis.
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1.05, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    ax.set_title('Area Change in Losses\n Case: ' + caseName)
    ax.set_xlim(0,minEnd)
    ax.set_ylabel('MW')
    ax.set_xlabel('Time [minutes]')

    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'AreaLosses'+'.pdf', dpi=300)
    plt.show(block=blkFlag)
    plt.pause(0.00001)