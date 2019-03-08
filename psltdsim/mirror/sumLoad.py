def sumLoad(mirror):
    """Returns system sums of active PSLF load as [Pload, Qload]"""
    Pload = 0.0
    Qload = 0.0
    for ndx in range(len(mirror.Load)):
        mirror.Load[ndx].getPvals()
        #Sum all loads with status == 1
        if mirror.Load[ndx].St == 1:
            Pload += mirror.Load[ndx].P
            Qload += mirror.Load[ndx].Q

    return [Pload,Qload]