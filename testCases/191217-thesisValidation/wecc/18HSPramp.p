/* Ramp of 3 loads +100 MW from t=2-42, accounts for prepending of 9 to bus */

/* ========================================================================= */
/* Standard loading of sav, dyd, and init of dynamic simulation */
@ret = getf("C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a.sav")

/* ========================================================================= */
/* Standard loading dyd, and init of dynamic simulation */
@ret = rdyd("C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1Fixed.dyd", "C:\LTD\pslf_systems\fullWecc\PSLFres\18HSPRamp.rep", "1")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

@ret = init("C:\LTD\pslf_systems\fullWecc\PSLFres\18HSPRamp.chf", "C:\LTD\pslf_systems\fullWecc\PSLFres\18HSPRamp.rep" , "1","0", "C:\LTD\inrun\wr1.p")

/* ========================================================================= */
/* Setting output resolution and simulation pauses */

dypar[0].nplot   = 1
dypar[0].nscreen = 240

@tpause = 1.9 
@tendRAMP =42.0
@tend =  90.0
@rampAMT = 100.0

/* ========================================================================= */
/* Tic - START TIMING */
@ret = tictoc(0)

/* Run Flat Lines For tpause seconds */
dypar[0].tpause  = @tpause
@ret = run()

/* ========================================================================= */
/* Collect initial values and calculate endvalues */

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
	@index1 = @returnVal
	@endVal1 = load[@index1].p + @rampAMT
	logterm("EndVal1 Calcualted, index stored.<")
endif 

@from = 924133

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Index found: ", @returnVal,"<")
	@index2 = @returnVal
	@endVal2 = load[@index2].p + @rampAMT
	logterm("EndVal2 Calcualted, index stored.<")
endif 

@from = 924135

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Index found: ", @returnVal,"<")
	@index3 = @returnVal
	@endVal3 = load[@index3].p + @rampAMT
	logterm("EndVal3 Calcualted, index stored.<")
endif 

/* ========================================================================= */
/* RUN FLAT LINES until ramp done. */
dypar[0].tpause  = @tendRAMP
@ret = run()     

/* ensure loads at propper end value*/
load[@index1].p = @endVal1
load[@index2].p = @endVal2
load[@index3].p = @endVal3

/* ========================================================================= */
/* RUN sim till tend*/
dypar[0].tpause  = @tend 
@ret = run()     

/* ========================================================================= */
/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()
/* Toc - DISPLAY TIMING */
@time = tictoc(1)
logterm("Elapsed time was ",@time,"<")
end
