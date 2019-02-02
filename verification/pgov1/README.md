pgov1_verification = initial system response to gov step (uses pgov1test and pgov1test2) (not used anymore)
pgov1_verification2 = system response to more correct pgov1 model - uses tests with Alpha
pgov1_verification3 = power and frequency response to steps - uses tests with Alpha

pgov1TestA = 1 second time step, 1 gov, 1 MW up, 1 MW down - 'ee554.exc.3.chf'
pgov1TestAab = A but with AB integration... breaks

pgov1TestB = 1 second time step, 2 gov, System Breaks -'ee554.exc.4.chf'

pgov1TestC = 0.5 second time step, 1 gov, 1 MW up, 1 MW down - 'ee554.exc.3.chf'
pgov1TestCab = 0.5 ab integration - works

pgov1TestD = 0.5 second time step, 2 gov, 1 MW up, 1 MW down - 'ee554.exc.4.chf'
pgov1TestDab = D with adams bashworth - breaks

pslf step tests at 2 and 30
'ee554.exc.3.chf' = 1 gov
'ee554.exc.4.chf' = 2 gov