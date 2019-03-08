def sumPm(mirror):
    """Returns sum of all mechanical power from active machines"""
    sysPm = 0.0
    for ndx in range(len(mirror.Machines)):
        #Sum all generator values if status = 1
        if mirror.Machines[ndx].St == 1:               
            sysPm += mirror.Machines[ndx].Pm

    return sysPm