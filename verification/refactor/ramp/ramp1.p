@ts = dypar[0].delt
@t = dypar[0].time

# logterm("Time Step: ",@ts, "<")
# logterm("Current Time: ",@t, "<")

if ((2< @t) and (@t <7 ))
	load[0].P = load[0].P - 2/5*@ts
	endif

if ((10< @t) and (@t <13))
	load[0].P = load[0].P + 1*@ts
	endif