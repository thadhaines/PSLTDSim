/* Step of 3 loads +100 MW at t=2, accounts for prepending of 9 to bus */

/* ========================================================================= */
/* Standard loading of sav, dyd, and init of dynamic simulation */
@ret = getf("C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a.sav")

/* ========================================================================= */
/* Standard loading dyd, and init of dynamic simulation */
@ret = rdyd("C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1Fixed.dyd", "C:\LTD\pslf_systems\fullWecc\PSLFres\18HSPStep.rep", "1")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

@ret = init("C:\LTD\pslf_systems\fullWecc\PSLFres\18HSPStep.chf", "C:\LTD\pslf_systems\fullWecc\PSLFres\18HSPStep.rep" , "1","0")


/* ========================================================================= */
/* Setting output resolution and simulation pauses */

dypar[0].nplot   = 1
dypar[0].nscreen = 240

@tpause = 2.0
@tend = 60.0

/* ========================================================================= */
/* Tic - START TIMING */
@ret = tictoc(0)

/* Run Flat Lines For tpause seconds */
dypar[0].tpause  = @tpause
@ret = run()

/* ========================================================================= */
/* Execute Perturbances */

@flag = 1 
@type = 4
@from = 924160
@to = -1
$ck = "**"
@sec = 0
@status = -1
@tert = -1

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Index found: ", @returnVal,"<")
	load[@returnVal].p = load[@returnVal].p + 100.0
	logterm("Pertrubance Executed.<")
endif 

@from = 924133

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Index found: ", @returnVal,"<")
	load[@returnVal].p = load[@returnVal].p + 100.0
	logterm("Pertrubance Executed.<")
endif 

@from = 924135

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Index found: ", @returnVal,"<")
	load[@returnVal].p = load[@returnVal].p + 100.0
	logterm("Pertrubance Executed.<")
endif 

/* ========================================================================= */
/* RUN sim till tend*/
@tpause = @tend
dypar[0].tpause  = @tpause  
@ret = run()     

/* ========================================================================= */
/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()
/* Toc - DISPLAY TIMING */
@time = tictoc(1)
logterm("Elapsed time was ",@time,"<")
end
