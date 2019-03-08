def dispSimResults(mirror):
    """Function to display running values to terminal"""
    for x in range(mirror.c_dp-1):
        if x%20 == 0:
            print("""Time\tPload\tPacc\tsys f\tdelta f\t\tSlackPe""")
        print("""%.2f\t%.2f\t%.2f\t%.5f\t%.6f\t%.2f""" % (
            mirror.r_t[x],
            mirror.r_ss_Pload[x],
            mirror.r_ss_Pacc[x],
            mirror.r_f[x],
            mirror.r_deltaF[x],
            mirror.Slack[0].r_Pe[x],))
    print('End of simulation data.')