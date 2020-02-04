def create_mirror_agents(mirror):
    """Create python mirror of PSLF system by 'crawling' 
    Handles Buses, Generators, and Loads
    Uses col
    TODO: Add agents for every object: shunts, SVD, xfmr, ...
    """
    # Useful variable notation key:
    # c_ .. current
    # f_ .. found
    # a_ .. area
    # n_ .. number of

    c_area = 0
    f_bus = 0
    i_bus = 0 # ignored island busses
    f_gen = 0
    f_load = 0
    f_shunt = 0
    mirror.ignoredBus = {}

    if mirror.debug: 
        print("*** Crawling system for agents...")
        print("Extnum\tgen\tload\tshunt\tBusnam")

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

                incRetCode = ltd.mirror.incorporate_bus(mirror, a_busses[c_bus], newAreaAgent)

                if incRetCode == 0:
                    # Count objects found on bus
                    c_ScanBus = a_busses[c_bus].GetScanBusIndex()
                    n_gen = col.GeneratorDAO.FindByBus(c_ScanBus).Count
                    n_load = col.LoadDAO.FindByBus(c_ScanBus).Count
                    n_shunt = col.ShuntDAO.FindAnyShuntsByBus(c_ScanBus).Count

                    f_gen += n_gen
                    f_load += n_load
                    f_shunt += n_shunt

                    if mirror.debug: 
                        print("%d\t%d\t%d\t%d\t%s" % 
                                         (a_busses[c_bus].Extnum, 
                                          n_gen, 
                                          n_load,
                                          n_shunt,
                                          a_busses[c_bus].Busnam)
                                         )
                else:
                    i_bus += 1 
                    mirror.ignoredBus[str(a_busses[c_bus].Extnum)] = a_busses[c_bus].Busnam
                    print("*** Ignoring bus %d %s - not in main island." % 
                          (a_busses[c_bus].Extnum, a_busses[c_bus].Busnam))

            mirror.Area.append(newAreaAgent)
        
        
        if n_branch > 0:
            for c_branch in range(n_branch):
                # check if branch connected to two valid busses
                fBus = int(col.BusDAO.FindByIndex(a_branches[c_branch].Ifrom).Extnum)
                tBus = int(col.BusDAO.FindByIndex(a_branches[c_branch].Ito).Extnum)
                validFbus = str(fBus) not in mirror.ignoredBus
                validTbus = str(tBus) not in mirror.ignoredBus
                if (validFbus == True) and  (validTbus == True):
                    #create branch agent
                    newBranch = ltd.systemAgents.BranchAgent(mirror, newAreaAgent, a_branches[c_branch])
                    #add branch to mirror
                    mirror.Branch.append(newBranch)
                    #add branch to area
                    newAreaAgent.Branch.append(newBranch)
                else:
                    print("*** Branch between %d and %d is islanded and ignored." % 
                          (fBus, tBus))
        
        c_area += 1
        
    # Assert: All busses in all areas are found and in mirror (else linking fails)
    if mirror.debug:
        print("***Creating %d branch links..." % len(mirror.Branch))

    for branch in mirror.Branch:
        branch.createLTDlinks()
        if branch.Islanded:
            mirror.Branch.remove(branch)
            print("*** Removed %s" % branch)

    # Init XFMRs in IPY
    if hasattr(mirror.simParams, 'makeXFMRs'):
        if mirror.simParams['makeXFMRs']:
            for area in mirror.Area:
                xfmrList = col.TransformerDAO.FindByArea(area.Area)
                for xfmr in xfmrList:
                    if xfmr.St == 1:
                        # Make Agent
                        newXFMRAgent = ltd.systemAgents.TransformerAgent(mirror, area, xfmr)
                        # Put links to agent in mirror
                        mirror.XFMR.append(newXFMRAgent)
                        area.XFMR.append(newXFMRAgent)
       

    if mirror.debug:
        print("Found %d Areas" % len(mirror.Area))
        print("Found %d buses" % f_bus)
        print("Ignored %d buses" % i_bus)
        print("Found %d gens (%d Slack)" % (f_gen, len(mirror.Slack)))
        print("Found %d loads" % f_load)
        print("Found %d shunts" % f_shunt)