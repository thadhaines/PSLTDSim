def create_mirror_agents(mirror):
    """Create python mirror of PSLF system by 'crawling' area busses
    Handles Buses, Generators, and Loads
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

    # while found buses are less than the total buses
    while f_bus < mirror.Nbus:
        # find and count buses in current area
        a_busses = col.AreaDAO.FindBusesInArea(c_area)
        n_bus = a_busses.Count

        # find branches in area
        a_branches = col.BranchDAO.FindByArea(c_area)
        n_branch = a_branches.Count

        # If Current area has buses, add to mirror
        if n_bus > 0:
            newAreaAgent = ltd.systemAgents.AreaAgent(mirror, c_area)
            f_bus += n_bus

            #for each found bus in area
            for c_bus in range(n_bus):
                
                ltd.mirror.incorporate_bus(mirror, a_busses[c_bus], newAreaAgent)
                c_ScanBus = a_busses[c_bus].GetScanBusIndex()

                n_gen = col.GeneratorDAO.FindByBus(c_ScanBus).Count
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
        
        if n_branch > 0:
            for c_branch in range(n_branch):
                #create branch agent
                newBranch = ltd.systemAgents.BranchAgent(mirror, newAreaAgent, a_branches[c_branch])
                #add branch to mirror
                mirror.Branch.append(newBranch)
                #add branch to area
                newAreaAgent.Branch.append(newBranch)
        
        c_area += 1

    # Assert: All busses in all areas are found and in mirror
    #for branch in mirror.Branch:
    #    branch.createLTDlinks()

    if mirror.debug:
        print("Found %d Areas" % len(mirror.Area))
        print("Found %d buses" % f_bus)
        print("Found %d gens (%d Slack)" % (f_gen, len(mirror.Slack)))
        print("Found %d loads" % f_load)