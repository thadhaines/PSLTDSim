def initInertiaH(mirror):
    """Link H and Mbase from PSLF dyd dynamic models to mirror machines
    Will calculate ss_H
    """
    # pdmod = pSLF dYNAMIC modLE
    if mirror.debug: print("*** Linking PSLF H to python environment...")
    linkedModels = 0

    for pdmod in range(len(mirror.PSLFmach)): # for each found pslf model
        mirrorGen = ltd.find.findGenOnBus(mirror, mirror.PSLFmach[pdmod].Busnum)

        if mirrorGen:
            mirrorGen.Hpu = mirror.PSLFmach[pdmod].H
            mirrorGen.MbaseDYD = mirror.PSLFmach[pdmod].Mbase
            # NOTE: PSLF .sav Mbase and .dyd Mbase may be different
            # dyd values overwrite any sav values (Via PSLF user manual)
            mirrorGen.H = mirror.PSLFmach[pdmod].H *mirror.PSLFmach[pdmod].Mbase
            mirror.ss_H += mirrorGen.H 
            # add refernece to PSLF machine model in python mirror
            mirrorGen.machine_model.append(mirror.PSLFmach[pdmod])
            if mirror.debug: print("PSLF model linked to %s" % mirrorGen)
            linkedModels +=1

    if mirror.debug: print("*** Linked %d/%d PSLF models to system." % (linkedModels,len(mirror.PSLFmach)))
