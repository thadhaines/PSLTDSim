def initInertiaH(mirror):
    """Link H and Mbase from PSLF dyd to mirror
    Calculate total system sum inertia (ss_H)
    """
    # pdmod = pSLF dYNAMIC modLE
    if mirror.debug: print("*** Linking PSLF H to python environment...")
    linkedModels = 0

    # for each found pslf machine model
    for pdmod in range(len(mirror.PSLFmach)): 

        mirrorGen = ltd.find.findGenOnBus(mirror, mirror.PSLFmach[pdmod].Busnum)

        if mirrorGen:
            # PSLF .sav values and .dyd values may be different
            # dyd values overwrite any sav values (Via PSLF user manual)
            if mirror.debug: print('*** Found H for: %s' % mirrorGen)
            mirrorGen.Hpu = mirror.PSLFmach[pdmod].H
            mirrorGen.Mbase = mirror.PSLFmach[pdmod].Mbase
            mirrorGen.H = mirror.PSLFmach[pdmod].H *mirror.PSLFmach[pdmod].Mbase
            mirror.ss_H += mirrorGen.H

            # add refernece to PSLF machine model in python mirror generator
            mirrorGen.machine_model = mirror.PSLFmach[pdmod]
            linkedModels +=1

            if mirror.debug: print("PSLF model linked to %s" % mirrorGen)

    if mirror.debug: print("*** Linked %d/%d PSLF models to system." 
                           % (linkedModels,len(mirror.PSLFmach)))
