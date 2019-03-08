def sumPe(mirror):
    """Returns sum of all electrical power from active machines
    Uses most recent PSLF values (update included in function)
    """
    sysPe = 0.0
    for ndx in range(len(mirror.Machines)):
        #Sum all generator values if status = 1
        if mirror.Machines[ndx].St == 1:
            mirror.Machines[ndx].getPvals()
            sysPe += mirror.Machines[ndx].Pe

    return sysPe

