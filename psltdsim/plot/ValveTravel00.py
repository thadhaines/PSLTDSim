def ValveTravel00(mirror, blkFlag=True, printFigs=False):
    """Plot ValveTravel of given mirror areas
    Same as ValveTravel, except internal legends.
    """
    import matplotlib.pyplot as plt
    from matplotlib.offsetbox import AnchoredText # for text box


    import numpy as np

    mir = mirror

    ### Plot Valve Travel, total in legend
    xend = max(mir.r_t)
    caseName = mir.simParams['fileName'][:-1]
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    mini = 1
    for area in mir.Area:
        fig, ax = plt.subplots()
        govMachines = 0 # for average movement
        aveTravel = 0

        for gen in area.Machines:
            if gen.gov_model:
                govMachines += 1
                totTravel = gen.gov_model.totValveMovement
                aveTravel += totTravel
                normVal = gen.gov_model.mwCap
                ax.plot(mins, np.array(gen.gov_model.r_x1)/normVal, linestyle = '-',linewidth=1,
                        label = 'Gen ' + str(gen.Busnum)+r'. Travel$_{total}$: '+str(round(totTravel,2))+' PU'  )
        
        if govMachines > 0:
            # Annotate average valve movement
            stringToPrint = "Average Area Travel "+str(round(aveTravel/govMachines,2))
            anchoredText = AnchoredText(stringToPrint, loc='upper right')
            ax.add_artist(anchoredText)


        ax.legend(loc='lower right', )

        ax.set_title(r'Area '+str(gen.Area)+' Valve Travel \n Case: ' + caseName)
        ax.set_xlim(0,minEnd)
        ax.set_ylabel('Valve Position [PU]')
        ax.set_xlabel('Time [minutes]')
        #ax.legend(loc=0)
        ax.grid(True)
        fig.set_dpi(150)
        fig.set_size_inches(9/mini, 2.5)
        fig.tight_layout()
        plt.show(block=blkFlag)
        if printFigs: plt.savefig(caseName+'ValveTravel'+str(gen.Area)+'.pdf', dpi=300)
        plt.pause(0.00001) # required for true non-blocking print...