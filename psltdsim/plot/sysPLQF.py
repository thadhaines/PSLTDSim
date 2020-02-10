def sysPLQF(mirror, blkFlag=True):
    """Plot System Pe, P_load; Qgen, and Frequency of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np # to ndarray.flatten ax

    mir = mirror
    xend = max(mir.r_t)

    fig, ax = plt.subplots(nrows=2, ncols=2,)
    ax = np.ndarray.flatten(ax)
    ax[0].set_title('Real Power Generated')
    for mach in mir.Machines:
        ax[0].plot(mir.r_t, mach.r_Pe, 
                    marker = 10,
                    fillstyle='none',
                    #linestyle = ':',
                    label = 'Pe Gen '+ mach.Busnam)
    ax[0].set_xlabel('Time [sec]')
    ax[0].set_ylabel('MW')

    ax[2].set_title('Reactive Power Generated')
    for mach in mir.Machines:
        ax[2].plot(mir.r_t, mach.r_Q, 
                    marker = 10,
                    fillstyle='none',
                    #linestyle = ':',
                    label = 'Q Gen '+ mach.Busnam)
    ax[2].set_xlabel('Time [sec]')
    ax[2].set_ylabel('MVAR')

    ax[1].set_title('Total System P Loading')
    ax[1].plot(mir.r_t, mir.r_ss_Pload, 
                marker = 11,
                #fillstyle='none',
                #linestyle = ':',
                label = 'Pload')
    ax[1].set_xlabel('Time [sec]')
    ax[1].set_ylabel('MW')

    ax[3].set_title('System Mean Frequency')
    ax[3].plot(mir.r_t, mir.r_f,
            marker = '.',
            #linestyle = ':',
            label = r'System Frequency')
    ax[3].set_xlabel('Time [sec]')
    ax[3].set_ylabel('Frequency [PU]')

    # Global Plot settings
    for x in np.ndarray.flatten(ax):
        x.set_xlim(0,xend)
        x.legend()
        x.grid(True)

    fig.tight_layout()

    plt.show(block = blkFlag)