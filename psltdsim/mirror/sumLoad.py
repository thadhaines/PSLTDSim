def sumLoad(mirror):
    """Returns system sums of active PSLF load as [Pload, Qload]"""
    sysPload = 0.0
    sysQload = 0.0
    # for each area
    for area in mirror.Area:
        # reset current sums
        area.P = 0.0
        area.Q = 0.0

        # sum each active load P and Q to area agent
        for load in area.Load:
            if load.St == 1:
                area.P += load.P
                area.Q += load.Q

        # sum area agent totals to system
        sysPload += area.P
        sysQload += area.Q

    return [sysPload,sysQload]