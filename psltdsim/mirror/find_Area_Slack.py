def find_Area_Slack(mirror):
    """Link each area to area slack"""
    for c_area in mirror.Area:
        areaObj = col.AreaDAO.FindByAreaNumber(c_area.Area)
        pslfSwingBus = col.BusDAO.FindByIndex(areaObj.Iswng)

        if pslfSwingBus:
            busGens = col.GeneratorDAO.FindByBus(pslfSwingBus)

            # assume only 1 slack gen on slack bus
            c_area.AreaSlack = ltd.find.findGenOnBus(mirror, 
                                                            pslfSwingBus.Extnum,
                                                            busGens[0].Id)
            c_area.AreaSlack.areaSlack = True

            if len(busGens) > 1:
                print('!!! Assumed first gen on area %d slack bus = slack gen' %
                      c_area.Area)
        else:
            print('*** Area %d Slack Not Defined!' % c_area.Area)
