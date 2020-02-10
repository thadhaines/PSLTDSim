def sysVmVAR(mirror, blkFlag=True):
    """Plot all Bus Vm and all generator MVAR output of given mirror"""
    import matplotlib.pyplot as plt

    mir = mirror
    xend = max(mir.r_t)

    fig, ax = plt.subplots(nrows=2, ncols=1,)
    ax[0].set_title('System Bus Voltage Magnitude')
    ax[0].grid(True)
    ax[1].set_title('System Bus Voltage Angle')
    ax[1].grid(True)
    for bus in mir.Bus:
        # choose marker based on bus type
        #none
        varMarker = "," # pixel
        busType = ""
        #load
        if bus.Nload > 0:
            varMarker = "v" # down triangle
            busType = "Load "

        #gen
        if bus.Ngen > 0:
            varMarker = "^"
            busType = "Gen "
        #slack
        if bus.Slack != []:
            varMarker = "o"
            busType = "Slack "

        ax[0].plot(mir.r_t, bus.r_Vm, 
                    marker = varMarker,
                    #fillstyle='none',
                    #linestyle = ':',
                    label = busType+'Bus '+ bus.Busnam)

    ax[1].set_title('Reactive Power Generated')
    for mach in mir.Machines:
        ax[1].plot(mir.r_t, mach.r_Q, 
                    marker = 10,
                    #fillstyle='none',
                    #linestyle = ':',
                    label = 'Q Gen '+ mach.Busnam + ' '+ mach.Id)

    ax[0].set_xlim(0,xend)
    ax[0].set_xlabel('Time [sec]')
    ax[0].set_ylabel('Voltage [PU]')
    ax[0].legend()

    ax[1].set_ylabel('MVAR')
    ax[1].set_xlabel('Time [sec]')
    ax[1].set_xlim(0,xend)
    ax[1].legend()

    fig.tight_layout()

    plt.show(block = blkFlag)
