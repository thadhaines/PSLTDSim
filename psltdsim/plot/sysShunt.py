def sysShunt(mirror, blkFlag=True, printFigs=False):
    """Plot system P and Q of active loading"""
    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror
    xend = max(mir.r_t)

    fig, ax = plt.subplots(nrows=2, ncols=1,)
    ax[0].set_title('Shunt Bus Voltage')
    ax[1].set_title('Shunt Bus Active B')

    # Shunts per bus
    for bus in mir.Bus:
        if len(bus.Shunt)>0:
            ax[0].plot(mir.r_t, bus.r_Vm, 
                    #marker = 'd',
                    #fillstyle='none',
                    #linestyle = ':',
                    label = 'Bus '+ str(bus.Extnum))
            busShuntTot = np.zeros_like(bus.Shunt[0].r_Q)
            for shunt in bus.Shunt:
                """
                ax[0].plot(mir.r_t, shunt.r_St, 
                    marker = 10,
                    linestyle = ':',
                    label = 'Shunt '+ str(shunt.FBusnum) +' Id ' + shunt.Id)
                """

                busShuntTot += shunt.r_Q

            ax[1].plot(mir.r_t, busShuntTot, 
                        #marker = 'd',
                        #fillstyle='none',
                        #linestyle = ':',
                        label = 'Bus '+ str(shunt.FBusnum) +' Total')

    ax[0].set_xlabel('Time [sec]')
    ax[0].set_ylabel('V [PU]')
    ax[1].set_xlabel('Time [sec]')
    ax[1].set_ylabel('MVAR')

    # Global Plot settings
    for x in np.ndarray.flatten(ax):
        x.set_xlim(0,xend)
        x.legend()
        x.grid(True)

    fig.tight_layout()

    plt.show(block = blkFlag)