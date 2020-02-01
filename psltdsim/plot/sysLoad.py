def sysLoad(mirror, blkFlag=True, printFigs=False):
    """Plot system P and Q of active loading"""
    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror
    xend = max(mir.r_t)

    fig, ax = plt.subplots(nrows=2, ncols=1,)
    ax[0].set_title('System P Load')
    ax[1].set_title('System Q Load')
    for load in mir.Load:
        ax[0].plot(mir.r_t, np.array(load.r_P)*np.array(load.r_St), 
                    #marker = 10,
                    #linestyle = ':',
                    label = 'Bus '+ load.Bus.Busnam +' Id ' + load.Id)
        ax[1].plot(mir.r_t, np.array(load.r_Q)*np.array(load.r_St), 
                    #marker = 'o',
                    #linestyle = ':',
                    label = 'Bus '+ load.Bus.Busnam +' Id ' + load.Id)
    # Shunts per bus
    for bus in mir.Bus:
        if len(bus.Shunt)>0:
            busShuntTot = np.zeros_like(bus.Shunt[0].r_Q)
            for shunt in bus.Shunt:
                busShuntTot += shunt.r_Q

            ax[1].plot(mir.r_t, busShuntTot, 
                        #marker = 'o',
                        #linestyle = ':',
                        label = 'Bus '+ str(shunt.FBusnum) +' Shunts')

    ax[0].set_xlabel('Time [sec]')
    ax[0].set_ylabel('MW')
    ax[1].set_xlabel('Time [sec]')
    ax[1].set_ylabel('MVAR')

    # Global Plot settings
    for x in np.ndarray.flatten(ax):
        x.set_xlim(0,xend)
        x.legend()
        x.grid(True)

    fig.tight_layout()

    plt.show(block = blkFlag)