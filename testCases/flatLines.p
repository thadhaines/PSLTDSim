/* Flat Lines for PSS init */

@tend = 60.0

/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\fullWecc\16HS\16HS3a.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\fullWecc\16HS\16HS31_dg.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\fullWecc\16HS\PSLFres\16HS3a_FL.chf", "C:\LTD\pslf_systems\fullWecc\16HS\PSLFres\16HS3a_FL.rep", 0, 1, "", "", 0)
dypar[0].nplot   = 3    
dypar[0].nscreen = 240*5

/* Tic */
@ret = tictoc(0)

/* RUN sim for 2 SEC */
dypar[0].tpause  = @tend  
@ret = run()    


/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()

/* Toc */
@time = tictoc(1)
logterm("Elapsed time was ",@time,"<")

end