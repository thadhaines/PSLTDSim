def sysPePmFLoad(mirror, blkFlag=True):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np

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
    if len(mir.Machines) < 5:
        # only make legend for smallish systems
        ax[0].legend()

    ax[1].set_title('System Mean Frequency and P Load')
    freq = ax[1].plot(mir.r_t, mir.r_f,
            color='k',
            marker = '.',
            #fillstyle='none',
            linestyle = ':',
            label = r'System Frequency')
    ax[1].set_xlabel('Time [sec]')
    ax[1].set_ylabel('Frequency [PU]')

    ax = np.append(ax, ax[1].twinx())

    loadCol = 'tab:blue'
    pload = ax[2].plot(mir.r_t, np.array(mir.r_ss_Pload)/mir.Sbase, 
                marker = 11,
                color = loadCol,
                #fillstyle='none',
                linestyle = ':',
                label = 'System P Load')
    ax[2].set_ylabel('MW [PU]', color = loadCol)
    ax[2].tick_params(axis='y', labelcolor = loadCol)

    lines = freq+pload
    labels = ['System Frequency', 'Pload']
    ax[1].legend(lines,labels)
    # Global plot settings
    for x in ax:
        x.set_xlim(0,xend)
        
        x.grid(True)

    fig.tight_layout()

    plt.show(block = blkFlag)