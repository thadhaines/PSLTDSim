def sumPm(mirror):
    """Returns sum of all mechanical power from active machines"""
    sysPm = 0.0

    # for each area
    for area in mirror.Area:
        # reset current sum
        area.cv['Pm'] = 0.0

        # sum each active machine Pm to area agent
        for mach in area.Machines:
            if mach.cv['St'] == 1:
                area.cv['Pm'] += mach.cv['Pm']

        # sum area agent totals to system
        sysPm += area.cv['Pm']

    return sysPm