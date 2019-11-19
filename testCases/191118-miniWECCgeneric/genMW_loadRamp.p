/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\miniWECC\miniWECC3AreaLTD.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\miniWECC\miniWECC_LTDgenerics.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\miniWECC\PSLFres\genMW_loadRamp.chf", "C:\LTD\pslf_systems\miniWECC\PSLFres\genMW_loadRamp.rep", 0, 1, "C:\LTD\inrun\mwr1.p", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 240*5   

/* Tic */
@ret = tictoc(0)

@EndVal5 = load[5].p +400
@EndVal2 = load[2].p +400
@EndVal3 = load[3].p +400

/* RUN FLAT LINES until ramp done. */
@tpause = 42.0
dypar[0].tpause  = @tpause  
@ret = run()     

/* ensure loads at propper end value*/
load[5].p = @EndVal5
load[2].p = @EndVal2
load[3].p = @EndVal3

/*  CONTINUE THE STABILITY RUN TO 90 SEC. */
@tpause = 120.0
dypar[0].tpause  = @tpause 
@ret = run()   

/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()
/* Toc */
@time = tictoc(1)
logterm("Elapse time is ",@time,"<")
end
