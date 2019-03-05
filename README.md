# PSLTDSim = Power System Long-Term Dynamic Simulator
Purpose:  Use Python 3 and PSLF to simulate long-term power system dynamics.
## Current Progress:
* Code creates python mirror of PSLF areas, busses, generators, and loads.
* Various functions have been written to:
  * Check accuracy of mirror
  * Parse .dyd files (more than one)
  * Handle H (inertia)
  * Add step perturbances to loads
  * Distribute changes in Pacc
  * Exectute Combined Swing equation
  * Step dynamic modles (pgov1)
  * Log values of interest
  * Generate data dictionary
  * Export Model or data data dictionary as a binary file (via pickle)
  * Import Model or data data dictionary into Python 3.x
  * Export Model or data data dictionary from Python 3.x to MATLAB .mat file
  * Generate terminal output
* MATLAB scripts created to verify simulation outputs of:
  * Combined swing equation to steps in load
  * pgov1 response to steps in load
  * Quick plot (LTDplot) of frequency, P and Q generated, System Loading, and Bus Voltage and Angles.
### Notes:
* To workaround GE API issues: Erlang, RabbitMQ, and Ironpython are required.
* Additional Python packages include:
    * Python 3: Numpy, Scipy, Pika
    * Ironpython: Pika
* For smaller test cases with only 1 Slack generator, the mirror seems to be 
accurate, however, for the full WECC (with 84 Slack generators), the global
system Slack has yet to be identified programmatically. 
While this will need to be resolved, other issues can be addressed in the meantime.
