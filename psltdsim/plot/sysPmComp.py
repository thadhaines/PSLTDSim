def sysPmComp(mirrorList, genNum, blkFlag=True, printFigs=False):
    """Plot  Pm of given gen mirrors"""
    import matplotlib.pyplot as plt
    import numpy as np
    import psltdsim as ltd

    plt.rcParams.update({'font.size': 9}) # used to scale text

    mini = 1 
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 2)

    colors=[ [0,0,0],
            [.7,.7,.7],
            [0,1,0],
            [1,0,1],
        ]
    styles =["-","--",':','-.'
        ]
    sNDX = 0

    for mirror in mirrorList:
        mir = ltd.data.readMirror(mirror)
        xend = max(mir.r_t)
        mini = 1 # can be increased to scale width of plots

        caseName = mir.simParams['fileName'][:-1]

        mins = np.array(mir.r_t)/60.0;
        minEnd = max(mins)

        ## Plot System Frequencies
        gen = ltd.find.findGenOnBus(mir,genNum)

        ax.plot(mins, gen.r_Pm,linewidth=1, 
                        #linestyle = '--',
                        label = caseName+' Pm')
        sNDX+=1

    ax.set_title('Controlled Generator Mechanical Power Output')
    ax.set_ylabel('Power [MW]')
    ax.set_xlabel('Time [minutes]')
    ax.set_xlim(0,minEnd)
    #ax.legend(loc='upper right')#, bbox_to_anchor=(0.5, -0.2))
    ax.legend()
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5) # single column, double height for legend below
    #fig.set_size_inches(9/2, 2.5*.75) # single column, double height for legend below
    fig.tight_layout()
    if printFigs: plt.savefig(caseName+'Gen'+str(genNum)+'Pm'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)