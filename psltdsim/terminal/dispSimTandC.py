def dispSimTandC(mir):
    """Display simulation timing and messages stats"""
    #NOTE: Handoff messages not included in message tally
    print('*** psltdsim.terminal.dispSimTandC(mirror)')
    print("*** Simulation Timings")
    #print('{:>22}'.format("Mirror Creation Time:") , '{:12f}'.format(mir.InitTime))

    print('{:>22}'.format("Total Simulation Time:") ,'      ', '{:12f}'.format(mir.SimTime))
    print('   ','{:>22}'.format("Dynamic CPU Time:") ,'  ', '{:12f}'.format(mir.DynamicTime))
    print('   ','{:>22}'.format("PY3 Send Time:") ,'  ','{:12f}'.format(mir.PY3SendTime))
    print('   ','{:>22}'.format("PY3 Recieve Time:") ,'  ','{:12f}'.format(mir.PY3RecTime))
    print('{:>22}'.format("Uncounted PY3 Time:") ,'      ', '{:12f}'.format(mir.SimTime-mir.DynamicTime-mir.PY3SendTime-mir.PY3RecTime))
    print('      ','{:>22}'.format("Power-Flow CPU Time:") , '{:12f}'.format(mir.PFTime))
    print('      ','{:>22}'.format("distPacc Time:") , '{:12f}'.format(mir.IPYdistPaccTime))
    print('      ','{:>22}'.format("PSLF Get/Set Time:") , '{:12f}'.format(mir.IPYPvalsTime))
    print('      ','{:>22}'.format("IPY Send Time:") , '{:12f}'.format(mir.IPYSendTime))
    print('{:>22}'.format("Uncounted IPY Time:") ,'      ', '{:12f}'.format(mir.PY3RecTime-mir.PFTime-mir.IPYSendTime-mir.IPYdistPaccTime-mir.IPYPvalsTime))
    


    print("\n*** Simulation Counters")    
    print('{:>22}'.format("Power-Flow Solutions:") , '{:12d}'.format(mir.PFSolns))
    print('{:>22}'.format("Sent PY3 Messages:") , '{:12d}'.format(mir.PY3msgs))
    print('{:>22}'.format("Sent IPY Messages:") , '{:12d}'.format(mir.IPYmsgs))
    print("\n*** Simulation etc") 
    print('{:>22}'.format("Simulated Time:") , '{:12f}'.format(mir.r_t[-1]))
    print('{:>22}'.format("Simulation Time Step:") , '{:12f}'.format(mir.timeStep))
    
