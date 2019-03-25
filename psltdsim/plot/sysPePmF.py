def sysPePmF(mirror, blkFlag=True):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt

    mir = mirror
    xend = max(mir.r_t)

    fig, ax = plt.subplots(nrows=2, ncols=1,)

    ax[0].set_title('Generator Power Distriubtion')
    for mach in mir.Machines:
        ax[0].plot(mir.r_t, mach.r_Pm, 
                 marker = 10,
                 fillstyle='none',
                 linestyle = ':',
                 label = 'Pm Gen '+ mach.Busnam)
        ax[0].plot(mir.r_t, mach.r_Pe, 
                 marker = 11,
                 linestyle = ':',
                 label = 'Pe Gen '+ mach.Busnam)
    ax[0].set_xlabel('Time [sec]')
    ax[0].set_ylabel('MW')


    ax[1].set_title('System Mean Frequency')
    ax[1].plot(mir.r_t, mir.r_f,
            marker = '.',
            fillstyle='none',
            linestyle = ':',
            label = r'System Frequency')
    ax[1].set_xlabel('Time [sec]')
    ax[1].set_ylabel('Frequency [PU]')

    # Global plot settings
    for x in ax:
        x.set_xlim(0,xend)
        x.legend()
        x.grid(True)

    fig.tight_layout()

    plt.show(block = blkFlag)