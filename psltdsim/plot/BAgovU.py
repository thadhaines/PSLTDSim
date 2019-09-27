def BAgovU(mirror, blkFlag=True, printFigs=False):
    """Plot Pe, Pm, and F of given mirror"""
    import matplotlib.pyplot as plt
    import numpy as np

    mir = mirror
    xend = max(mir.r_t)
    mini = 1 # can be increased to scale width of plots

    caseName = mir.simParams['fileName'][:-1]
    # Plot controlled machines Pref and Pm
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    firstPlot = True

    for BA in mir.BA:
        fig, ax = plt.subplots()
        for gen in BA.ctrlMachines:
            uInput = gen.gov_model.r_u
            ax.plot(mins, uInput, linestyle = '-',linewidth=1,
                    label = r'$U $  '+str(gen.Busnum)+' '+gen.Id)
        
        if firstPlot:
            # Scale current axis.
            box = ax.get_position()
            boxW = box.width * 1.05
            firstPlot = False

        ax.set_position([box.x0, box.y0, boxW, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        ax.set_title(r'Area '+str(gen.Area)+' ('+ BA.name + ') Controlled Machines U input \n Case: ' + caseName)
        ax.set_xlim(0,minEnd)
        ax.set_ylabel('Input [MW]')
        ax.set_xlabel('Time [minutes]')
        #ax.legend(loc=0)
        ax.grid(True)
        fig.set_dpi(150)
        fig.set_size_inches(9/mini, 2.5)
        fig.tight_layout()
        plt.show(block=False)
        if printFigs: plt.savefig(caseName+BA.name+'U.pdf', dpi=300)
        plt.pause(0.00001) # required for true non-blocking print...

    plt.show(block = blkFlag)
    plt.pause(0.00001)