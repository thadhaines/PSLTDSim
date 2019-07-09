#epcl item iteration test

for @i = 0 to casepar[0].nload-1
	logterm("load index ",@i," has p = ",load[@i].p," and q = ",load[@i].q,"<")
next

for @i = 0 to casepar[0].ngen-1
	logterm("gen index ",@i," has p = ",gens[@i].pgen," and q = ",gens[@i].qgen,"<")
next

for @i = 0 to casepar[0].nshunt-1
	logterm("shunt index ",@i," has b = ",shunt[@i].b," and g = ",shunt[@i].g,"<")
next

#epcl item scaling test
@scale = 0.95
for @i = 0 to casepar[0].nload-1
	load[@i].p = load[@i].p*@scale
	load[@i].q = load[@i].q*@scale
	logterm("load index ",@i," has p = ",load[@i].p," and q = ",load[@i].q,"<")
next

for @i = 0 to casepar[0].ngen-1
	gens[@i].pgen = gens[@i].pgen*@scale
	gens[@i].qgen = gens[@i].qgen*@scale
	logterm("gen index ",@i," has p = ",gens[@i].pgen," and q = ",gens[@i].qgen,"<")
next

for @i = 0 to casepar[0].nshunt-1
	shunt[@i].b=shunt[@i].b*@scale
	shunt[@i].g=shunt[@i].g*@scale
	logterm("shunt index ",@i," has b = ",shunt[@i].b," and g = ",shunt[@i].g,"<")
next