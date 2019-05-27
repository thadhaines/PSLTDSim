def dispSimTandC(mir):
    """Display simulation timing and messages stats"""
    #NOTE: Handoff messages not included in message tally
    print('*** psltdsim.terminal.dispSimTandC(mirror)')
    #print('{:>28}'.format("Mirror Creation Time:") , '{:12f}'.format(mir.InitTime))

    print('{:<28}'.format("Simulation Timings"))
    print('{:>28}'.format("Total Simulation Time:") , '{:12f}'.format(mir.SimTime))
    print('{:>28}'.format("PY3 Dynamics CPU Time:") , '{:12f}'.format(mir.DynamicTime))
    print('{:>28}'.format("PY3 Send Time:") ,'{:12f}'.format(mir.PY3SendTime))
    print('{:>28}'.format("PY3 Find Time:") ,'{:12f}'.format(mir.FindTime))
    #print('{:>28}'.format("PY3 Recieve Time:") ,'{:12f}'.format(mir.PY3RecTime))
    print('{:>28}'.format("IPY Find Time:") ,'{:12f}'.format(mir.IPYFindTime))
    print('{:>28}'.format("IPY distPacc Time:") , '{:12f}'.format(mir.IPYdistPaccTime))
    print('{:>28}'.format("IPY PSLF Get/Set Time:") , '{:12f}'.format(mir.IPYPvalsTime))
    print('{:>28}'.format("IPY Msg Make Time:") , '{:12f}'.format(mir.IPYmsgMake))
    print('{:>28}'.format("IPY Send Time:") , '{:12f}'.format(mir.IPYSendTime))
    print('{:>28}'.format("Uncounted PY3 Time:") , '{:12f}'.format(mir.SimTime-mir.DynamicTime-mir.PY3SendTime-mir.PY3RecTime-mir.FindTime))
    print('{:>28}'.format("Uncounted IPY Time:") , '{:12f}'.format(mir.PY3RecTime-mir.PFTime-mir.IPYSendTime-mir.IPYdistPaccTime-mir.IPYPvalsTime-mir.IPYmsgMake-mir.IPYFindTime))
    print('{:>28}'.format("PSLF Power-Flow Time:") , '{:12f}'.format(mir.PFTime))

    print('{:<28}'.format("Simulation Counters"))
    print('{:>28}'.format("Sent PY3 Messages:") , '{:12d}'.format(mir.PY3msgs))
    print('{:>28}'.format("Sent IPY Messages:") , '{:12d}'.format(mir.IPYmsgs))
    print('{:>28}'.format("Power-Flow Solutions:") , '{:12d}'.format(mir.PFSolns))
    print('{:<28}'.format("Simulation Summary"))

    print('{:>28}'.format("Real time Speedup:") , '{:12f}'.format(mir.r_t[-1]/mir.SimTime))
    print('{:>28}'.format("Ave. PY3 msg send:") , '{:12f}'.format(mir.PY3SendTime/mir.PY3msgs))
    print('{:>28}'.format("Ave. IPY msg send:") , '{:12f}'.format(mir.IPYSendTime/mir.IPYmsgs))
    print('{:>28}'.format("Ave Power-Flow Time:") , '{:12f}'.format(mir.PFTime/mir.PFSolns))
    print('{:>28}'.format("Ave. P-F / Time Step:") , '{:12f}'.format(mir.PFSolns/mir.c_dp))
    print('{:>28}'.format("Simulated Time:") , '{:12f}'.format(mir.r_t[-1]))
    print('{:>28}'.format("Simulation Time Step:") , '{:12f}'.format(mir.timeStep))