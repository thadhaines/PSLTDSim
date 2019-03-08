def dispCaseParams(model):
    """Display current Case Parameters"""
    print("*** Case Parameters ***")
    print(".sav ==\t%s" % model.locations[2])
    print("%d Areas" % model.Narea)
    print("%d Zones" % model.Nzone)
    print("%d Busses" % model.Nbus)
    print("%d Generators" % model.Ngen)
    print("%d Loads" % model.Nload)
    print("***_________________***")
