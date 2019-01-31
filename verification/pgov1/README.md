pgov1_verification = initial system response to gov step (uses pgov1test and pgov1test2) (not used anymore)
pgov1_verification2 = system response to more correct pgov1 model - uses tests with Alpha
pgov1_verification3 = power and frequency response to steps - uses tests with Alpha


pgov1TestA = 1 second time step, 1 gov, 1 MW up, 1 MW down - 'ee554.exc.3.chf'
pgov1TestB = 1 second time step, 2 gov, System Breaks
pgov1TestC = 0.5 second time step, 1 gov, 1 MW up, 1 MW down - 'ee554.exc.3.chf'
pgov1TestBhres = 0.5 second time step, 2 gov, 1 MW up, 1 MW down - 'ee554.exc.4.chf'
pgov1TestD - same as test Bhres with Pe = Pm after dynamics

pgov1TestE - same as test B with Pe = Pm after dynamics - still likes to blow up

pgov1TestA1 = same as A, Pe = Pm added to code - seems 'swingyer'
pgov1TestA2 = same as A, Pe = (Pe+Pm)/2 added to code - seems less peaky than A1
pgov1TestC1 = same as C, Pe = Pm
pgov1TestC2 = same as C, Pe = (Pe+Pm)/2 added to code - seems less peaky than A1

pgov1TestB1 = same as B, Pe = (Pe+Pm)/2 added to code - system still breaks.
pgov1TestB1a = same as B, Pe = (Pe+Pm)/2 added to code - ts = 0.5 - doesnt brak

pslf step tests at 2 and 30
'ee554.exc.3.chf' = 1 gov
'ee554.exc.4.chf' = 2 gov