/* Tripping 2 lines off at t=2, then one back on at t=60*/

@tend = 90.0

/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\sixMachine\sixMachineTrips.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\sixMachine\sixMachine2.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. Third field from end (2nd quote from end) is where inrun epcl paths go*/
@ret = init("C:\LTD\pslf_systems\sixMachine\results\sixMachineBranchTrip1.chf", "C:\LTD\pslf_systems\sixMachine\results\sixMachineBranchTrip1.rep", 0, 1, "", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 240*5

/* Tic */
@ret = tictoc(0)

/* RUN sim for 2 SEC */
@tpause = 2.0
dypar[0].tpause  = @tpause  
@ret = run()    

/* Execute Perturbance */
@flag = 1 
@type = 1
@from = 8
@to = 9
$ck = "2"
@sec = 1
@status = 0
@tert = -1

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Pertrubance Executed.<")
endif 

/* Execute Perturbance */
@flag = 1 
@type = 1
@from = 8
@to = 9
$ck = "3"
@sec = 1
@status = 0
@tert = -1

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Pertrubance Executed.<")
endif 

/* RUN sim till  next Pertrubance*/
@tpause = 60
dypar[0].tpause  = @tpause  
@ret = run()  
/* Execute Perturbance */
@flag = 1 
@type = 1
@from = 8
@to = 9
$ck = "2"
@sec = 1
@status = 1
@tert = -1

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Pertrubance Executed.<")
endif 


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