def initRunningVals(mirror):
    """Initialize History Values of mirror"""
    #TODO: use numpy arrays instead
    # initialize running (history) values 
    mirror.r_t = [0.0]*mirror.dataPoints

    mirror.r_f = [0.0]*mirror.dataPoints
    mirror.r_deltaF = [0.0]*mirror.dataPoints
    mirror.r_fdot = [0.0]*mirror.dataPoints

    mirror.r_ss_Pe = [0.0]*mirror.dataPoints
    mirror.r_ss_Pm = [0.0]*mirror.dataPoints
    mirror.r_ss_Pacc = [0.0]*mirror.dataPoints
    mirror.r_Pacc_delta = [0.0]*mirror.dataPoints

    mirror.r_ss_Qgen = [0.0]*mirror.dataPoints
    mirror.r_ss_Qload = [0.0]*mirror.dataPoints
    mirror.r_ss_Pload = [0.0]*mirror.dataPoints

    # for fun stats, not completely utilized - yet
    mirror.PLosses = 0.0
    mirror.QLosses = 0.0
    mirror.r_PLosses = [0.0]*mirror.dataPoints
    mirror.r_QLosses = [0.0]*mirror.dataPoints
