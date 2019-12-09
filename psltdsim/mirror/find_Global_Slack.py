def find_Global_Slack(mirror):
    """Locates and sets the global slack generator"""
    # Collect all slack bus in system
    zBus = col.BusDAO.FindByType(0)
    gSlackB = None

    if len(zBus) == 1:
        # If only 1 slack, obvious choice
        gSlackB = zBus[0]
    else:
        for bus in zBus:
            #print("** slack bus debug:  %s  -isl: %d  -stIsol %d" %(bus, bus.Islnum, bus.Stisol))
            if bus.Islnum == 1:
                # otherwise, find slack in island 1
                gSlackB = bus

    if gSlackB == None:
        # island number doesn't result with unique slack...
        for bus in zBus:
            if bus.Stisol == 0:
                # work around for mysteryWECC case
                gSlackB = bus

    print('*** Global Slack bus: %d %s' % (gSlackB.Extnum, gSlackB.Busnam))

    countAtBus = col.GeneratorDAO.CountAtBus(gSlackB)
    if countAtBus == 1:
        # all tested cased only have 1 generator at this point.
        #gen = col.GeneratorDAO.FindByBus(gSlackB)
        mirrorGen = ltd.find.findGenOnBus(mirror, gSlackB.Extnum)
        mirrorGen.globalSlack = True
        mirror.globalSlack = mirrorGen
        return

    """
    # old
    if len(mirror.Slack) < 2:
        mirror.Slack[0].globalSlack = True
        mirror.globalSlack = mirror.Slack[0]
    else:
        print("More than 1 slack generator found... Setting first to global... ")
        mirror.Slack[0].globalSlack = True
        mirror.globalSlack = mirror.Slack[0]
    """