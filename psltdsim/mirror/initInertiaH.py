def initInertiaH(mirror):
    """Link H and Mbase from PSLF dyd to mirror
    Calculate total system sum inertia (ss_H)
    """
    # pdmod = pSLF dYNAMIC modLE
    if mirror.debug: print("*** Linking PSLF H to python environment...")
    linkedModels = 0

    for pdmod in mirror.PSLFmach: 

        # Check if Model is for a Generator
        if pdmod.isMachine:
            mirrorGen = ltd.find.findGenOnBus(mirror, pdmod.Busnum, pdmod.Id)

            if mirrorGen:
                # PSLF .sav values and .dyd values may be different
                # dyd values overwrite any sav values (Via PSLF user manual)
                if mirror.debug: print('*** Found H for: %s' % mirrorGen)
                mirrorGen.Hpu = pdmod.H
                mirrorGen.Mbase = pdmod.Mbase
                mirrorGen.H = pdmod.H *pdmod.Mbase
                mirror.ss_H += mirrorGen.H

                # add refernece to PSLF machine model in python mirror generator
                mirrorGen.machine_model = pdmod
                linkedModels +=1
            
        if mirror.debug: print("PSLF Machine model linked to %s" % mirrorGen)

    if mirror.debug: print("*** Linked %d/%d PSLF models to system." 
                           % (linkedModels,len(mirror.PSLFmach)))
