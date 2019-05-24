def dispSimTandC(mir):
    """Display simulation timing and messages stats"""
    #NOTE: Handoff messages not included in message tally
    print("\n*** Simulation Timings and Counters")
    print("Mirror Creation Time:\t %f" % mir.InitTime )
    print("Total Simulation Time:\t %f" % mir.SimTime )
    print("Simulated Time:\t\t %.2f" % mir.r_t[-1] )
    print("Simulation Time Step:\t %.2f" % mir.timeStep )
    print("\n*** PSLF Timings and Counters")
    print("Power-Flow CPU Time:\t %f" % mir.PFTime )
    print("Power-Flow Solutions:\t %d" % mir.PFSolns )
    print("\n*** AMQP Timings and Counters")
    print("Sent PY3 Messages:\t %d" % mir.PY3msgs )
    print("PY3 Message Time:\t %f" % mir.PY3SendTime )
    print("Sent IPY Messages:\t %d" % mir.IPYmsgs )
    print("IPY Message Time:\t %f" % mir.IPYSendTime )