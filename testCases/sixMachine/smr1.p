/* Six Machine ramp of load 9 +s10% */
@ts = dypar[0].delt
@t = dypar[0].time
@init = 1

if ((2 > @t) and (1.8 < @t))
	/* Calcualte ramp params */
	@flag = 1
	@type = 4
	@from = 9
	@to = -1
	$ck = "1"
	@sec = 0
	@status = -1
	@tert = -1

	@index = rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
	@startP = load[@index].p
	@increment = ((@startP*1.1)-@startP)/40.0*@ts
	endif

if ((2< @t) and (@t <42 ))
	load[@index].p = load[@index].p + @increment
	endif
