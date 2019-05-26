def dispSimResults(mirror):
    """Function to display running values to terminal"""
    print('*** psltdsim.terminal.dispSimResults(mirror)') # for added
    for x in range(len(mirror.r_t)):
        if x%20 == 0:
            print('{:>12s}\t{:>12s}\t{:>12s}\t{:>12s}\t{:>12s}\t{:>12s}\t'.format('Time','Pload','Pacc','Sys f','Delta f','Slack Pe',))
        print('{:12f}\t{:12f}\t{:12f}\t{:12f}\t{:12f}\t{:12f}'.format(mirror.r_t[x], mirror.r_ss_Pload[x], mirror.r_ss_Pacc[x], mirror.r_f[x], mirror.r_deltaF[x], mirror.Slack[0].r_Pe[x],))

    print('End of simulation data.\n')