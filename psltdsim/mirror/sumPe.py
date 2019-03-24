def sumPe(mirror):
    """Returns sum of all electrical power from active machines"""
    sysPe = 0.0

    # for each area
    for area in mirror.Area:
        # reset current sum
        area.Pe = 0.0

        # sum each active machine Pe to area agent
        for mach in area.Machines:
            if mach.St == 1:
                area.Pe += mach.Pe

        # sum area agent totals to system
        sysPe += area.Pe

    return sysPe

