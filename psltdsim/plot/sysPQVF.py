def sysPQVF(mirror):
    """Plot P, Q, Gen bus Voltage, and F of given mirror"""
    import matplotlib.pyplot as plt

    mir = mirror
    fig, ax = plt.subplots(nrows=2, ncols=2,)
    ax[0][0].set_title('Real Power Generated')
    ax[0][0].grid(True)
    for mach in mir.Machines:
        ax[0][0].plot(mir.r_t, mach.r_Pe, 
                    marker = 10,
                    linestyle = ':',
                    label = 'Pe Gen '+ mach.Busnam)
    ax[0][0].set_xlabel('Time [sec]')
    ax[0][0].set_ylabel('MW')
    ax[0][0].legend()

    ax[0][1].set_title('Reactive Power Generated')
    ax[0][1].grid(True)
    for mach in mir.Machines:
        ax[0][1].plot(mir.r_t, mach.r_Q, 
                    marker = 10,
                    linestyle = ':',
                    label = 'Q Gen '+ mach.Busnam)
    ax[0][1].set_xlabel('Time [sec]')
    ax[0][1].set_ylabel('MVAR')
    ax[0][1].legend()

    ax[1][0].set_title('Generator Bus Voltage Magnitude')
    ax[1][0].grid(True)
    for gen in mir.Machines:
        ax[1][0].plot(mir.r_t, mach.Bus.r_Vm, 
                    marker = 10,
                    linestyle = ':',
                    label = 'Gen Bus '+ mach.Busnam)
    ax[1][0].set_xlabel('Time [sec]')
    ax[1][0].set_ylabel('Voltage [PU]')
    ax[1][0].legend()

    ax[1][1].set_title('System Mean Frequency')
    ax[1][1].grid(True)
    ax[1][1].plot(mir.r_t, mir.r_f,
            marker = '.',
            linestyle = ':',
            label = r'System Frequency')
    ax[1][1].set_xlabel('Time [sec]')
    ax[1][1].set_ylabel('Frequency [PU]')
    ax[1][1].legend()

    fig.tight_layout()

    plt.show()