/* Ramp load on bus 9 up 10% at t=2 to t=42*/

@tend = 120.0

/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\sixMachine\sixMachineTrips.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\sixMachine\sixMachine.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. Third field from end (2nd quote from end) is where inrun epcl paths go*/
@ret = init("C:\LTD\pslf_systems\sixMachine\PSLFres\sixMachineRamp1.chf", "C:\LTD\pslf_systems\sixMachine\PSLFres\sixMachineRamp1.rep", 0, 1, "C:\LTD\inrun\smr1.p", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 240*5

/* Tic */
@ret = tictoc(0)

/* Find initial P value */
@flag = 1
@type = 4
@from = 9
@to = -1
$ck = "1"
@sec = 0
@status = -1
@tert = -1

@index = rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)

@initP = load[@index].p

/* RUN sim  */
@tpause = 42.0
dypar[0].tpause  = @tpause  
@ret = run()    

/* Ensure end ramp value */
load[@index].p = @initP * 1.1

/* RUN sim for rest of sim*/
@tpause = @tend
dypar[0].tpause  = @tpause  
@ret = run()     

/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()

/* Toc */
@time = tictoc(1)
logterm("Elapsed time was ",@time,"<")

end