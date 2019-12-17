/* Six Machine ramp of load 9 +s10% */
@ts = dypar[0].delt
@t = dypar[0].time
@init = 1

if ((2 > @t) and (1.8 < @t))
	/* Calcualte ramp params load 16*/
	@flag = 1
	@type = 4
	@from = 16
	@to = -1
	$ck = "1"
	@sec = 0
	@status = -1
	@tert = -1

	@index16 = rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
	@startP = load[@index16].p
	@increment16 = ((@startP+400)-@startP)/40.0*@ts

	/* Calcualte ramp params load 21 */
	@flag = 1
	@type = 4
	@from = 21
	@to = -1
	$ck = "1"
	@sec = 0
	@status = -1
	@tert = -1

	@index21 = rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
	@startP = load[@index21].p
	@increment21 = ((@startP+400)-@startP)/40.0*@ts

	/* Calcualte ramp params load 26 */
	@flag = 1
	@type = 4
	@from = 26
	@to = -1
	$ck = "1"
	@sec = 0
	@status = -1
	@tert = -1

	@index26 = rec_index(@flag,@type,@from,@to,$ck,@sec,@status,@tert)
	@startP = load[@index26].p
	@increment26 = ((@startP+400)-@startP)/40.0*@ts

	endif

if ((2< @t) and (@t <42 ))
	load[@index16].p = load[@index16].p + @increment16
	load[@index21].p = load[@index21].p + @increment21
	load[@index26].p = load[@index26].p + @increment26
	endif
