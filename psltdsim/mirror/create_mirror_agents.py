def create_mirror_agents(mirror):
    """Create python mirror of PSLF system by 'crawling' area busses
    Handles Buses, Generators, and Loads
    WAS init_mirror
    Uses col
    TODO: Add agents for every object: shunts, SVD, xfmr, branch sections, ...
    """
    # Useful variable notation key:
    # c_ .. current
    # f_ .. found
    # a_ .. area
    # n_ .. number of

    c_area = 0
    f_bus = 0
    f_gen = 0
    f_load = 0

    if mirror.debug: 
        print("*** Crawling system for agents...")
        print("Extnum\tgen\tload\tBusnam")

    while f_bus < mirror.Nbus:
        #while not all busses are found
        a_busses = col.AreaDAO.FindBusesInArea(c_area)
        #n_bus = len(a_busses)
        n_bus = a_busses.Count
        if n_bus > 0:
            #If Current area has buses
            newAreaAgent = ltd.systemAgents.AreaAgent(mirror, c_area)
            f_bus += n_bus

            for c_bus in range(n_bus):
                #for each found bus
                ltd.mirror.incorporate_bus(mirror, a_busses[c_bus], newAreaAgent)
                c_ScanBus = a_busses[c_bus].GetScanBusIndex()
                #n_gen = len(col.GeneratorDAO.FindByBus(c_ScanBus))
                n_gen = col.GeneratorDAO.FindByBus(c_ScanBus).Count
                #n_load = len(col.LoadDAO.FindByBus(c_ScanBus))
                n_load = col.LoadDAO.FindByBus(c_ScanBus).Count

                f_gen += n_gen
                f_load += n_load

                if mirror.debug: 
                    print("%d\t%d\t%d\t%s" % 
                                     (a_busses[c_bus].Extnum, 
                                      n_gen, 
                                      n_load,
                                      a_busses[c_bus].Busnam)
                                     )
            mirror.Area.append(newAreaAgent)
        c_area += 1
    
    if mirror.debug:
        print("Found %d Areas" % len(mirror.Area))
        print("Found %d buses" % f_bus)
        print("Found %d gens (%d Slack)" % (f_gen, len(mirror.Slack)))
        print("Found %d loads" % f_load)