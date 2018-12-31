# LTD_sim
Goal:  Use Ironpython and PSLF to simulate longterm dynamics.
## Current Progress:
* Code creates python mirror of PSLF areas, busses, generators, and loads.
* Various functions have been written to:
  * Check accuracy of mirror
  * Parse .dyd files
  * Handle H (inertia)
  * Add perturbances to loads
  * Log values of interest
  * Generate terminal output
### Notes:
* For smaller test cases with only 1 Slack generator, the mirror seems to be 
accurate, however, for the full WECC (with 84 Slack generators), the global
system Slack has yet to be identified programmatically. 
While this will need to be resolved, other issues can be addressed in the meantime.
