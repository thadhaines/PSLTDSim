/* Kundur ramp of load 9 30% */
@ts = dypar[0].delt
@t = dypar[0].time

if ((2 > @t))
	@startP = load[2].p
	@increment = ((@startP*1.3)-@startP)/85.0*@ts
	endif

if ((2<= @t) and (@t <=87 ))
	load[2].p = load[2].p + @increment
	endif
