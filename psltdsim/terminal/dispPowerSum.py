def dispPowerSum(model):
    """Display System Sumation power values"""
    print("*** System Power Overview ***")
    print("Pm:\t%.3f" % model.ss_Pm)
    print("Pe:\t%.3f" % model.ss_Pe)
    print("Pacc:\t%.3f" % model.ss_Pacc)
    print("Pload:\t%.3f" % model.ss_Pload)
    print("Ploss:\t%.3f" % model.PLosses)
    print("*_*")
    #NOTE: Q values are meaningless until Shunts and SVDs are accounted for
    print("Qgen:\t%.3f" % model.ss_Qgen)
    print("Qload:\t%.3f" % model.ss_Qload)
    print("Qloss:\t%.3f" % model.QLosses)
    print("***_______________________***")