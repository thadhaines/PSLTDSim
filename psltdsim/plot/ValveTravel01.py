def ValveTravel01(mirror, blkFlag=True, printFigs=False):
    """Plot ValveTravel of given mirror areas"""
    import matplotlib.pyplot as plt
    from matplotlib.offsetbox import AnchoredText # for text box


    import numpy as np

    mir = mirror

    ### Plot Valve Travel, total in legend
    xend = max(mir.r_t)
    caseName = mir.simParams['fileName'][:-1]
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    firstPlot = True
    mini = 1
    fig, ax = plt.subplots()
    aveTravel = []
    curArea = 0
    stringsToPrint = []

    for area in mir.Area:
        govMachines = 0 # for average movement
        aveTravel.append(0.0)

        for gen in area.Machines:

            if gen.gov_model:
                govMachines += 1
                totTravel = gen.gov_model.totValveMovement
                aveTravel[curArea] += totTravel
                normVal = gen.gov_model.mwCap
                travelString = (r'Gen %3d Travel$_{total}$: %.2f PU' % (gen.Busnum,totTravel) )
                ax.plot(mins, np.array(gen.gov_model.r_x1)/normVal, linestyle = '-',linewidth=1,
                        label = travelString)
                        #'Gen ' + str(gen.Busnum)+r' Travel$_{total}$: '+str(round(totTravel,2))+' PU'  )
        
        if govMachines > 0:
            # Annotate average valve movement
            stringsToPrint.append( "Average Area "+str(gen.Area) +" Travel "+str(round(aveTravel[curArea]/govMachines,2)) )

        #if firstPlot:
        #    # Scale current axis.
        #    box = ax.get_position()
        #    boxW = box.width * 1.05
        #    firstPlot = False

        curArea+= 1

    combSTR = ''
    for areaSTR in stringsToPrint:
        combSTR = combSTR + areaSTR +'\n'

    combSTR = combSTR[:-1] # remove extra \n

    anchoredText = AnchoredText(combSTR, loc='upper left',
                                prop=dict(fontsize="large"),
                                )
    ax.add_artist(anchoredText)
    #ax.set_position([box.x0, box.y0, boxW, box.height])

    # Put a legend to the right of the current axis
    #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend(loc='lower right')

    ax.set_title('Valve Travel \n Case: ' + caseName)
    ax.set_xlim(0,minEnd)
    ax.set_ylim(0,1.2)
    ax.set_ylabel('Valve Position [PU]')
    ax.set_xlabel('Time [minutes]')
    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9, 2.5)
    #fig.set_size_inches(5.5, 4.5)
    #fig.set_size_inches(9, 4.5)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'ValveTravel01.pdf', dpi=300)
    plt.show(block=blkFlag)
    plt.pause(0.00001) # required for true non-blocking print...