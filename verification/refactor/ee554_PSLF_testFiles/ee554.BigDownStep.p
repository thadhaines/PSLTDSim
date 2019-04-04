/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\eele554\ee554.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\eele554\ee554.excNoGov.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\eele554\PSLFres\ee554.BigDownStep.chf", "C:\LTD\pslf_systems\eele554\PSLFres\ee554.BigDownStep.rep", 0, 1, "", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 3    

/* RUN FLAT LINES FOR 2 SEC. */
@tpause = 2.0
dypar[0].tpause  = @tpause  
@ret = run()     

/* step load up 1 mw */
load[0].p = load[0].p -20

/*  CONTINUE THE STABILITY RUN TO 20 SEC. */
@tpause = 20.0
dypar[0].tpause  = @tpause 
@ret = run()     

/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()

end
