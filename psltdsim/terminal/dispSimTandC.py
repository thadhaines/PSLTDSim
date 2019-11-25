def dispSimTandC(mir):
    """Display simulation timing and messages stats"""
    #NOTE: Handoff messages not included in message tally /send time
    print('\n*** psltdsim.terminal.dispSimTandC(mirror)')
    print('*** File name: %s\n' % mir.simParams['fileName'])
    print('{:<28}'.format("Simulation Timings"))
    print('{:>28}'.format("Total Simulation Time:") , '{:12f}'.format(mir.SimTime))
    print('{:>28}'.format("PY3 IVP CPU Time:") , '{:12f}'.format(mir.IVPTime))
    print('{:>28}'.format("PY3 Dynamics CPU Time:") , '{:12f}'.format(mir.DynamicTime))
    print('{:>28}'.format("PY3 Message Send Time:") ,'{:12f}'.format(mir.PY3SendTime))
    print('{:>28}'.format("PY3 Agent Find Time:") ,'{:12f}'.format(mir.FindTime))
    #print('{:>28}'.format("PY3 Recieve Time:") ,'{:12f}'.format(mir.PY3RecTime)) # confusing time for unknowing
    print('{:>28}'.format("IPY Agent Find Time:") ,'{:12f}'.format(mir.IPYFindTime))
    print('{:>28}'.format("IPY distPacc Time:") , '{:12f}'.format(mir.IPYdistPaccTime))
    print('{:>28}'.format("IPY PSLF Get/Set Time:") , '{:12f}'.format(mir.IPYPvalsTime))
    print('{:>28}'.format("IPY Message Make Time:") , '{:12f}'.format(mir.IPYmsgMake))
    print('{:>28}'.format("IPY Message Send Time:") , '{:12f}'.format(mir.IPYSendTime))
    print('{:>28}'.format("Uncounted PY3 Time:") , '{:12f}'.format(mir.SimTime-mir.DynamicTime-mir.PY3SendTime-mir.PY3RecTime-mir.IVPTime)) #mir.FindTime
    print('{:>28}'.format("Uncounted IPY Time:") , '{:12f}'.format(mir.PY3RecTime-mir.PFTime-mir.IPYSendTime-mir.IPYdistPaccTime-mir.IPYPvalsTime-mir.IPYmsgMake)) #mir.IPYFindTime
    print('{:>28}'.format("PSLF Power-Flow Time:") , '{:12f}'.format(mir.PFTime))

    print('{:<28}'.format("Simulation Counters"))
    print('{:>28}'.format("Sent PY3 Messages:") , '{:12d}'.format(mir.PY3msgs))
    print('{:>28}'.format("Sent IPY Messages:") , '{:12d}'.format(mir.IPYmsgs))
    print('{:>28}'.format("PY3 Dynamic Solutions:") , '{:12d}'.format(mir.DynamicSolns))
    print('{:>28}'.format("Power-Flow Solutions:") , '{:12d}'.format(mir.PFSolns))

    print('{:<28}'.format("Simulation Summary"))
    if len(mir.r_t) > 0:
        print('{:>28}'.format("Real time Speedup:") , '{:12f}'.format(mir.r_t[len(mir.r_t)-1]/mir.SimTime))
    print('{:>28}'.format("Ave. PY3 msg send:") , '{:12f}'.format(mir.PY3SendTime/mir.PY3msgs))
    print('{:>28}'.format("PY3 Message Group Size:") , '{:12d}'.format(mir.PY3msgGroup))
    if mir.IPYmsgs>0:
        print('{:>28}'.format("Ave. IPY msg send:") , '{:12f}'.format(mir.IPYSendTime/mir.IPYmsgs))
    print('{:>28}'.format("IPY Message Group Size:") , '{:12d}'.format(mir.IPYmsgGroup))

    if mir.DynamicSolns >0: # handle cases with no dynamics
        print('{:>28}'.format("Ave. Dynamic Soln. Time:") , '{:12f}'.format(mir.DynamicTime/mir.DynamicSolns))
    else:
        print('{:>28}'.format("Ave. Dynamic Soln. Time:") , '{:12f}'.format(0.0))

    print('{:>28}'.format("Ave Power-Flow Time:") , '{:12f}'.format(mir.PFTime/mir.PFSolns))
    if mir.cv['dp']>0:
        print('{:>28}'.format("Ave. P-F / Time Step:") , '{:12f}'.format(mir.PFSolns/mir.cv['dp']))
    print('{:>28}'.format("Mirror Creation Time:") , '{:12f}'.format(mir.InitTime))
    if len(mir.r_t) > 0:
        print('{:>28}'.format("Simulated Time:") , '{:12f}'.format(mir.r_t[len(mir.r_t)-1]))
    print('{:>28}'.format("Simulation Time Step:") , '{:12f}'.format(mir.timeStep))