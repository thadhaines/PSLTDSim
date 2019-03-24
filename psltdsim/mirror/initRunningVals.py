def initRunningVals(mirror, PY3flag = False):
    """Initialize History Values of mirror NOT USED ATM"""
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

    if PY3flag:
        # Use numpy arrays instead of lists
        # Maybe a future python 3 only solution - not used ATM
        mirror.r_t = np.array(mirror.r_t)

        mirror.r_f = np.array(mirror.r_f)
        mirror.r_deltaF = np.array(mirror.r_deltaF)
        mirror.r_fdot = np.array(mirror.r_fdot)

        mirror.r_ss_Pe = np.array(mirror.r_ss_Pe)
        mirror.r_ss_Pm = np.array(mirror.r_ss_Pm)
        mirror.r_ss_Pacc = np.array(mirror.r_ss_Pacc)
        mirror.r_Pacc_delta = np.array(mirror.r_Pacc_delta)

        mirror.r_ss_Qgen = np.array(mirror.r_ss_Qgen)
        mirror.r_ss_Qload = np.array(mirror.r_ss_Qload)
        mirror.r_ss_Pload = np.array(mirror.r_ss_Pload)

        # for fun stats, not completely utilized - yet
        mirror.PLosses = 0.0
        mirror.QLosses = 0.0
        mirror.r_PLosses = np.array(mirror.r_PLosses)
        mirror.r_QLosses = np.array(mirror.r_QLosses)
