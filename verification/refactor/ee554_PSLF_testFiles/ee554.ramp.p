/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\eele554\ee554.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\eele554\ee554.exc.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\eele554\PSLFres\ee554.ramp2.chf", "C:\LTD\pslf_systems\eele554\PSLFres\ee554.ramp2.rep", 0, 1, "C:\LTD\inrun\r1.p", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 3    

/* RUN FLAT LINES FOR 2 SEC. */
@tpause = 2.0
dypar[0].tpause  = @tpause  
@ret = run()     

/*  CONTINUE THE STABILITY RUN TO 21 SEC. */
@tpause = 21.0
dypar[0].tpause  = @tpause 
@ret = run()     
load[0].p = load[0].p - 1

/*  CONTINUE THE STABILITY RUN TO 30 SEC. */
@tpause = 40.0
dypar[0].tpause  = @tpause 
@ret = run()  

/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()

end
