/* ramp of wecc loads over 40 seconds */
@ts = dypar[0].delt
@t = dypar[0].time
@init = 1
@rampAMT = 100.00 	/* Full ramp change */
@rampTIME = 40.0	/* Total Ramp time */

/* Calculate relative ramp increments */
if ((2 > @t) and (1.8 < @t))
	/* Calcualte ramp params load 924160*/
	@flag = 1 
	@type = 4
	@from = 924160
	@to = -1
	$ck = "**"
	@sec = 0
	@status = -1
	@tert = -1

	@index1 = rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
	@startP = load[@index1].p
	@increment1 = ((@startP+@rampAMT)-@startP)/@rampTIME*@ts

	/* Calcualte ramp params load 924133 */
	@from = 924133
	@index2 = rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
	@startP = load[@index2].p
	@increment2 = ((@startP+@rampAMT)-@startP)/@rampTIME*@ts

	/* Calcualte ramp params load 924135 */
	@from = 924135
	@index3 = rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
	@startP = load[@index3].p
	@increment3 = ((@startP+@rampAMT)-@startP)/@rampTIME*@ts

	endif
/* Execute ramp increments */
if ((2< @t) and (@t <42 ))
	load[@index1].p = load[@index1].p + @increment1
	load[@index2].p = load[@index2].p + @increment2
	load[@index3].p = load[@index3].p + @increment3
	endif
