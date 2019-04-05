/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\eele554\ee554.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\eele554\ee554.exc1Gov.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\eele554\PSLFres\ee554.ramp0.chf", "C:\LTD\pslf_systems\eele554\PSLFres\ee554.ramp0.rep", 0, 1, "C:\LTD\inrun\r0.p", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 3    



/*  CONTINUE THE STABILITY RUN TO 30 SEC. */
@tpause = 30.0
dypar[0].tpause  = @tpause 
@ret = run()  

/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()

end
