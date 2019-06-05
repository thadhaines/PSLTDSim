def sumLoad(mirror):
    """Returns system sums of active PSLF load as [Pload, Qload]"""
    sysPload = 0.0
    sysQload = 0.0
    # for each area
    for area in mirror.Area:
        # reset current sums
        area.cv['P'] = 0.0
        area.cv['Q'] = 0.0

        # sum each active load P and Q to area agent
        for load in area.Load:
            if load.cv['St'] == 1:
                area.cv['P'] += load.cv['P']
                area.cv['Q'] += load.cv['Q']

        # sum area agent totals to system
        sysPload += area.cv['P']
        sysQload += area.cv['Q']

    return [sysPload,sysQload]