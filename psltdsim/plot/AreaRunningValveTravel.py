def AreaRunningValveTravel(mirror, blkFlag=True, printFigs=False):
    """Plot AreaLosses of given mirror areas"""
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams.update({'font.size': 9}) # used to scale text

    mir = mirror
    ### Plot Area Change in Losses over time
    mins = np.array(mir.r_t)/60.0;
    minEnd = max(mins)
    caseName = mir.simParams['fileName'][:-1]
    mini = 1

    colors=[ [0,0,0],
            [.7,.7,.7],
            [0,1,0],
            [1,0,1],
        ]
    styles =["-","--",':','-.'
        ]
    sNDX = 0
    
    fig, ax = plt.subplots()

    for area in mir.Area:
        areaSum = np.zeros_like(mir.r_t)
        nGen = 0
        for gen in area.Gens:
            if gen.gov_model:
                areaSum+= gen.gov_model.r_valveTravel
                nGen += 1

        ax.plot(mins, areaSum/nGen, linewidth=1.25, 
                linestyle=styles[sNDX],
                color=colors[sNDX],
                label= 'Area '+ str(area.Area))
        sNDX+=1

    # Scale current axis.
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 1.05, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='upper left')#, bbox_to_anchor=(1, 0.5))

    ax.set_title('Average Valve Travel Over Time')
    ax.set_xlim(0,minEnd)
    ax.set_ylabel('PU')
    ax.set_xlabel('Time [minutes]')

    #ax.legend(loc=0)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/2, 2.5*.75)
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'VTOverTime'+'.pdf', dpi=300)
    plt.show(block=blkFlag)
    plt.pause(0.00001)