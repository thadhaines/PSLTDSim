/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\miniWECC\miniWECC3AreaLTD.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\miniWECC\miniWECC_LTDgenerics.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\miniWECC\PSLFres\genMW_loadStep.chf", "C:\LTD\pslf_systems\miniWECC\PSLFres\genMW_loadStep.rep", 0, 1, "", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 240*5   

/* Tic */
@ret = tictoc(0)

/* RUN FLAT LINES FOR 2 SEC. */
@tpause = 2.0
dypar[0].tpause  = @tpause  
@ret = run()     

/* step oregon load way up*/
load[5].p = load[5].p +400
load[2].p = load[2].p +400
load[3].p = load[3].p +400

/*  CONTINUE THE STABILITY RUN TO 90 SEC. */
@tpause = 90.0
dypar[0].tpause  = @tpause 
@ret = run()   

/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()
/* Toc */
@time = tictoc(1)
logterm("Elapse time is ",@time,"<")
end
