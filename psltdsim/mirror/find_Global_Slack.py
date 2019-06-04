def find_Global_Slack(mirror):
    """Locates and sets the global slack generator"""
    #NOTE: Not even close to complete

    zBus = col.BusDAO.FindByType(0)
    if len(zBus) == 1:
        gSlackB = zBus[0]
    else:
        for bus in zBus:
            if bus.Islnum == 1:
                gSlackB = bus

    print('Global Slack bus %d %s' % (gSlackB.Extnum, gSlackB.Busnam))

    countAtBus = col.GeneratorDAO.CountAtBus(gSlackB)
    if countAtBus == 1:
        gen = col.GeneratorDAO.FindByBus(gSlackB)


    if len(mirror.Slack) < 2:
        mirror.Slack[0].globalSlack = True
        mirror.globalSlack = mirror.Slack[0]
    else:
        print("More than 1 slack generator found... Setting first to global... ")
        mirror.Slack[0].globalSlack = True
        mirror.globalSlack = mirror.Slack[0]