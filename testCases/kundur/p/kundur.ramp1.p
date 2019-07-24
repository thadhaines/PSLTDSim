/* Kundur ramp EPCL */
/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\kundur4LTD\kundur4LTD.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\kundur4LTD\kundur4LTDsameGens.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\kundur4LTD\results\kundur.ramp1.chf", "C:\LTD\pslf_systems\kundur4LTD\results\kundur.ramp1.rep", 0, 1, "C:\LTD\inrun\kr1.p", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 240   


/* Ensuring area interchange is off (as possible?) */
solpar[0].aiadj = 0
solpar[0].aiopt = 0

/* Tic */
@ret = tictoc(0)

/* RUN sim for 15 SEC to . */
@tpause = 90.0
dypar[0].tpause  = @tpause  
@ret = run()     

/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()

/* Toc */
@time = tictoc(1)
logterm("Elapse time is ",@time,"<")

@inter = solpar[0].aiadj
@opt = solpar[0].aiopt

logterm("aiadj is ",@inter,"<")
logterm("aiopt is ",@opt,"<")
end