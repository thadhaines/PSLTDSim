def dispSimResults(mirror):
    """Function to display running values to terminal"""
    print('*** psltdsim.terminal.dispSimResults(mirror)') # for added
    for x in range(len(mirror.r_t)):
        if x%20 == 0:
            print('{:>13s}\t{:>13s}\t{:>13s}\t{:>13s}\t{:>13s}\t{:>13s}\t{:>13s}\t'.format('____',
                                                                                           '_____',
                                                                                           '____',
                                                                                           '_______'
                                                                                           ,'_____'
                                                                                           ,'________'
                                                                                           ,'________',))
            print('{:>13s}\t{:>13s}\t{:>13s}\t{:>13s}\t{:>13s}\t{:>13s}\t{:>13s}\t'.format('Time',
                                                                                           'Pload',
                                                                                           'Pacc',
                                                                                           'PaccDot'
                                                                                           ,'Sys f'
                                                                                           ,'Sys fDot'
                                                                                           ,'Slack Pe',))
        print('{:13f}\t{:13f}\t{:13f}\t{:13f}\t{:13f}\t{:13f}\t{:13f}'.format(mirror.r_t[x], 
                                                                      mirror.r_ss_Pload[x], 
                                                                      mirror.r_ss_Pacc[x], 
                                                                      (mirror.r_ss_Pacc[x]-mirror.r_ss_Pacc[x-1])/mirror.timeStep, 
                                                                      mirror.r_f[x], 
                                                                      mirror.r_fdot[x], 
                                                                      mirror.Slack[0].r_Pe[x],))

    print('End of simulation data.\n')