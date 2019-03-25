def sysVmVa(mirror, blkFlag=True):
    """Plot all Bus Vm and Va of given mirror"""
    import matplotlib.pyplot as plt

    mir = mirror
    xend = max(mir.r_t)

    fig, ax = plt.subplots(nrows=2, ncols=1,)
    ax[0].set_title('System Bus Voltage Magnitude')
    ax[0].grid(True)
    ax[1].set_title('System Bus Voltage Angle')
    ax[1].grid(True)
    for bus in mir.Bus:
        ax[0].plot(mir.r_t, bus.r_Vm, 
                    marker = 10,
                    fillstyle='none',
                    linestyle = ':',
                    label = 'Bus '+ bus.Busnam)
        ax[1].plot(mir.r_t, bus.r_Va, 
                    marker = 'o',
                    fillstyle='none',
                    linestyle = ':',
                    label = 'Bus '+ bus.Busnam)
    ax[0].set_xlabel('Time [sec]')
    ax[0].set_xlim(0,xend)
    ax[0].set_ylabel('Voltage [PU]')
    ax[0].legend()

    ax[1].set_xlabel('Time [sec]')
    ax[1].set_xlim(0,xend)
    ax[1].set_ylabel('Voltage Anlge [PU]')
    ax[1].legend()

    fig.tight_layout()

    plt.show(block = blkFlag)
