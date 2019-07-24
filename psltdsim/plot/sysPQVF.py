def sysPQVF(mirror, blkFlag=True):
    """Plot P, Q, Gen bus Voltage, and F of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np # to flatten ax

    mir = mirror
    xend = max(mir.r_t)

    fig, ax = plt.subplots(nrows=2, ncols=2,)

    ax[0][0].set_title('Real Power Generated')
    for mach in mir.Machines:
        ax[0][0].plot(mir.r_t, mach.r_Pe, 
                    #marker = 10,
                    fillstyle='none',
                    linestyle = ':',
                    label = 'Pe Gen '+ mach.Busnam)
    ax[0][0].set_xlabel('Time [sec]')
    ax[0][0].set_ylabel('MW')

    ax[0][1].set_title('Reactive Power Generated')
    for mach in mir.Machines:
        ax[0][1].plot(mir.r_t, mach.r_Q, 
                    #marker = 10,
                    fillstyle='none',
                    linestyle = ':',
                    label = 'Q Gen '+ mach.Busnam)
    for shunt in mir.Shunt:
        if not all(v == 0 for v in shunt.r_Q):
            ax[0][1].plot(mir.r_t, shunt.r_Q, 
                        #marker = 10,
                        fillstyle='none',
                        linestyle = '-',
                        label = 'Q SVD '+ shunt.Bus.Busnam + ' ' +shunt.Id)
    ax[0][1].set_xlabel('Time [sec]')
    ax[0][1].set_ylabel('MVAR')

    ax[1][1].set_title('Bus Voltage Magnitude')
    for bus in mir.Bus:
        ax[1][1].plot(mir.r_t, bus.r_Vm, 
                    #marker = 10,
                    fillstyle='none',
                    linestyle = ':',
                    label = 'Bus '+ bus.Busnam)
    ax[1][1].set_xlabel('Time [sec]')
    ax[1][1].set_ylabel('Voltage [PU]')

    ax[1][0].set_title('System Mean Frequency')
    ax[1][0].plot(mir.r_t, mir.r_f,
            #marker = '.',
            #linestyle = ':',
            label = r'System Frequency')
    ax[1][0].set_xlabel('Time [sec]')
    ax[1][0].set_ylabel('Frequency [PU]')

    # Global Plot settings
    for x in np.ndarray.flatten(ax):
        x.set_xlim(0,xend)
        x.legend(loc=1)
        x.grid(True)

    fig.tight_layout()

    plt.show(block = blkFlag)

    if not blkFlag:
        plt.pause(0.00001) # required for true non-blocking print...