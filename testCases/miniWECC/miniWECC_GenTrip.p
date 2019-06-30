/* Tripping Generator on bus 5 (90 MW) at t=2*/

@tend = 180.0

/* Open .sav file */
@ret = getf("C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC.sav")

/* MAKE SURE BASE CASE IS SOLVED. */
@ret = soln()

/* READ THE DYNAMIC DATA. */
@ret = rdyd("C:\LTD\pslf_systems\MiniPSLF_PST\miniWECCLTD3.dyd","",1)

/* INIT THE DYNAMIC DATA AND SET THE CHANNEL FILE. */
@ret = init("C:\LTD\pslf_systems\MiniPSLF_PST\PSLFres\miniWECC_genTrip0.chf", "C:\LTD\pslf_systems\eele554\PSLFres\miniWECC_genTrip0.rep", 0, 1, "", "", 0)
dypar[0].nplot   = 1     
dypar[0].nscreen = 240*5

/* Tic */
@ret = tictoc(0)

/* RUN sim for 2 SEC */
@tpause = 2.0
dypar[0].tpause  = @tpause  
@ret = run()    

/* Execute Perturbance */
@flag = 1 
@type = 3
@from = 27
@to = -1
$ck = "**"
@sec = 0
@status = 0
@tert = -1

@returnVal= rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
if (@returnVal<0)
	logterm("Error in Locating Perturbance Target.<")
else
	logterm("Pertrubance Executed.<")
endif 

/* RUN sim for rest of sim*/
@tpause = @tend
dypar[0].tpause  = @tpause  
@ret = run()     

/*  CLOSE THE CHANNEL FILE. */
@ret = dsst()

/* Toc */
@time = tictoc(1)
logterm("Elapsed time was ",@time,"<")

end