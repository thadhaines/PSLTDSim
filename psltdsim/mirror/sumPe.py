def sumPe(mirror):
    """Returns sum of all electrical power from active machines"""
    sysPe = 0.0

    # for each area
    for area in mirror.Area:
        # reset current sum
        area.cv['Pe'] = 0.0

        # sum each active machine Pe to area agent
        for mach in area.Machines:
            if mach.cv['St'] == 1:
                area.cv['Pe'] += mach.cv['Pe']

        # sum area agent totals to system
        sysPe += area.cv['Pe']

    return sysPe

