def sysPePmFLoad(mirror, blkFlag=True):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.cm import get_cmap

    name = "tab20"
    cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
    colors = cmap.colors  # type: list
    #print(colors)
    mir = mirror
    xend = max(mir.r_t)

    fig, ax = plt.subplots(nrows=2, ncols=1,)
    for subfig in ax:
        subfig.set_prop_cycle(color=colors)

    if len(mir.Machines) < 7:
        normalizeFlag = False
    else:
        legendFlag = False
        normalizeFlag = True

    if len(mir.Machines) <10:
        legendFlag = True
 
    if normalizeFlag:
        ax[0].set_title('Normalized Generator Electrical Power Change')
        for mach in mir.Machines:
            ax[0].plot(mir.r_t, (np.array(mach.r_Pe)/mach.r_Pe[0]-1)*100.00, 
                     #marker = 11,
                     ##linestyle = ':',
                     linewidth = 1,
                     label = 'Pe Gen '+ mach.Busnam)
        ax[0].set_ylabel('% MW Change')
                     
    else:
        ax[0].set_title('Generator Power Distriubtion')
        for mach in mir.Machines:
            ax[0].plot(mir.r_t, mach.r_Pe, 
                     #marker = 11,
                     #inestyle = '--',
                     linewidth = 2,
                     label = r'$P_e$ Gen '+ mach.Busnam)
            ax[0].plot(mir.r_t, mach.r_Pm, 
                     #marker = 10,
                     fillstyle='none',
                     #linestyle = '--',
                     linewidth = 1,
                     label = r'$P_m$ Gen '+ mach.Busnam)
        ax[0].set_ylabel('MW')

    ax[0].set_xlabel('Time [sec]')

    if legendFlag:
        # only make legend for smallish systems
        ax[0].legend(loc=1)

    ax[1].set_title('System Mean Frequency and P Load')
    freq = ax[1].plot(mir.r_t, mir.r_f,
            color='k',
            #marker = '.',
            #fillstyle='none',
            #linestyle = ':',
            label = r'System Frequency')
    ax[1].set_xlabel('Time [sec]')
    ax[1].set_ylabel('Frequency [PU]')

    ax = np.append(ax, ax[1].twinx())

    loadCol = 'tab:blue'
    pload = ax[2].plot(mir.r_t, mir.r_ss_Pload, 
                #marker = 11,
                color = loadCol,
                #fillstyle='none',
                #linestyle = ':',
                label = 'System P Load')
    ax[2].set_ylabel('MW', color = loadCol)
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

    if not blkFlag:
        plt.pause(0.00001) # required for true non-blocking print...