def sysShuntMVAR(mirror, blkFlag=True, printFigs=False):
    """Plot mvar of system Shunt buses 
    uses cycler for color and style - repeats after 6
    """
    
    import matplotlib.pyplot as plt
    from matplotlib.offsetbox import AnchoredText # for text box
    import numpy as np
    # custom color cycler
    from cycler import cycler
    ltdColors=[ [0,0,0], # black
            [.7,.7,.7], # grey
            [0,1,0], # green
            [1,0,1], # magenta
            "#17becf", # light blue
            [1,.647,0],# orange
        ]
    ltdStyles =  ["-","--",':',"-","--",':']
    default_cycler = ( cycler(color=ltdColors)  + cycler(linestyle=ltdStyles) )
    plt.rc('axes', prop_cycle=default_cycler)

    mir = mirror

    ### Plot Valve Travel, total in legend
    xend = max(mir.r_t)
    caseName = mir.simParams['fileName'][:-1]
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    mini = 1


    fig, ax = plt.subplots()
    ax.set_title('Shunt Bus Voltage')

    # Shunts per bus
    for bus in mir.Bus:
        if len(bus.Shunt)>0:
            busShuntTot = np.zeros_like(bus.Shunt[0].r_Q)
            for shunt in bus.Shunt:
                busShuntTot += shunt.r_Q

            ax.plot(mins, busShuntTot, 
                        #marker = 'd',
                        #fillstyle='none',
                        #linestyle = ':',
                        label = 'Bus '+ str(shunt.FBusnum) +' Total')

    

    ax.legend(loc='upper left', )

    ax.set_title('Shunt Bus Active B\n Case: ' + caseName)
    ax.set_xlim(0,minEnd)
    ax.set_xlabel('Time [minutes]')
    ax.set_ylabel('MVAR')
    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    plt.show(block=blkFlag)
    if printFigs: plt.savefig(caseName+'sysShuntMVAR'+'.pdf', dpi=300)
    plt.pause(0.00001) # required for true non-blocking print...