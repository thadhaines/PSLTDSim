/* Kundur ramp EPCL -5% from t=2 to t=42 */
/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\kundur4LTD\kundur4LTD.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\kundur4LTD\kundur4LTDsameGens.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\kundur4LTD\results\kundur.ramp0.chf", "C:\LTD\pslf_systems\kundur4LTD\results\kundur.ramp0.rep", 0, 1, "C:\LTD\inrun\kr0.p", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 5   

/* Ensuring area interchange is off (as possible?) */
solpar[0].aiadj = 0
solpar[0].aiopt = 0

/* Checking in run file maths */
@ts = dypar[0].delt
@startP = load[2].p
@increment = -((@startP*1.05)-@startP)/40.0*@ts

/* Tic */
@ret = tictoc(0)

/* RUN sim for 42 SEC,  ensure ramp ends at the correct spot. . */
@tpause = 42.0
dypar[0].tpause  = @tpause  
@ret = run()     
load[2].p = 855.00

/* RUN sim for 42 SEC,  ensure ramp ends at the correct spot. . */
@tpause = 80.0
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
logterm("ramp increment was ",@increment,"<")
logterm("Simulation timestep is ",@ts,"<")
end