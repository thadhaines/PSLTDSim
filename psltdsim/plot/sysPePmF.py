def sysPePmF(mirror):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt

    mir = mirror

    fig, ax = plt.subplots(nrows=2, ncols=1,)
    ax[0].set_title('Generator Power Distriubtion')
    ax[0].grid(True)
    for mach in mir.Machines:
        ax[0].plot(mir.r_t, mach.r_Pm, 
                 marker = 10,
                 linestyle = ':',
                 label = 'Pm Gen '+ mach.Busnam)
        ax[0].plot(mir.r_t, mach.r_Pe, 
                 marker = 11,
                 linestyle = ':',
                 label = 'Pe Gen '+ mach.Busnam)
    ax[0].set_xlabel('Time [sec]')
    ax[0].set_ylabel('MW')
    ax[0].legend()


    ax[1].set_title('System Mean Frequency')
    ax[1].grid(True)
    ax[1].plot(mir.r_t, mir.r_f,
            marker = '.',
            linestyle = ':',
            label = r'System Frequency')
    ax[1].set_xlabel('Time [sec]')
    ax[1].set_ylabel('Frequency [PU]')
    ax[1].legend()

    fig.tight_layout()

    plt.show()