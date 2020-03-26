def genDynamicsComp(mirList, blkFlag=True, printFigs = False, genNum = 0):
    """Plot all dynamic responses from generators
    does not block by default - blkFlag ignored
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import psltdsim as ltd
    plt.rcParams.update({'font.size': 9}) # used to scale text

    fig, ax = plt.subplots()

    colors=[ [0,0,0],
            [.7,.7,.7],
            [0,1,0],
            [1,0,1],
        ]
    styles =["-",
             "--",
             (0,(1,1)),
             '-.'
        ]

    sNDX = 0

    for mirror in mirList:

        mir = ltd.data.readMirror(mirror)
        mins = np.array(mir.r_t)/60.0;
        minEnd = max(mins)
        # label for data plot
        dbTypeSTR ='None'
        dbType = mir.BA[0].BAdict['GovDeadbandType']

        if dbType.lower() == 'nldroop':
            dbTypeSTR ='Non-Linear'

        if dbType.lower() == 'step':
            dbTypeSTR ='Step'

        if dbType.lower() == 'ramp':
            dbTypeSTR ='No-Step'

        # Handle bad input
        cGen = ltd.find.findGenOnBus(mir, genNum, None, False)
        if cGen == None:
            print("No generator found on bus %d." % genNum)
            return

        if cGen.gov_model == False:
            print("Generator on bus %d has no governor." % genNum)
            return
        
        normVal = cGen.gov_model.mwCap
        ax.plot(mins, np.array(cGen.gov_model.r_x1)/normVal,  
                        linestyle=styles[sNDX],
                        color=colors[sNDX],
                    #label = 'Travel: '+ str(round(cGen.gov_model.totValveMovement,2)) + ' Deadband: ' + dbTypeSTR )
                    label = 'Deadband: ' + dbTypeSTR )
        sNDX+=1
    ax.set_title('Generator on Bus %d Valve Travel' 
                % (cGen.Busnum,))
    ax.set_xlabel('Time [minutes]')
    ax.set_ylabel('Valve Position [PU]')
    # Global Plot settings

    ax.set_xlim(0,3)
    ax.legend(loc='upper right')#, bbox_to_anchor=(0.5, -0.2))

    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9, 2.5) # single column, double height for legend below
    fig.tight_layout()
    if printFigs: plt.savefig('gen'+str(genNum)+'ValveComp'+'.pdf', dpi=300)
    plt.show(block = blkFlag)
    plt.pause(0.00001)