# LTD_sim
Goal:  Using Ironpython, communicate with PSLF to simulate longterm dynamics.
## Current Progress:
* Code creates python mirror of PSLF generators, loads, and busses.
* Various functions have been written to:
  * Check accuracy of mirror
  * Parse .dyd files
  * Add perturbances to loads
  * Log values of interest
  * Generate terminaloutput
### Notes:
* For smaller test cases with only 1 Slack generator, the mirror seems to be 
accurate, however, for the full WECC (with 84 Slack generators), the global
system Slack has yet to be identified programmatically. While this will need to be resolved, other issues may be addresssed.

