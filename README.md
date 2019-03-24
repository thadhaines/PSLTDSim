# PSLTDSim = Power System Long-Term Dynamic Simulator
Purpose:  Use Python 3 and PSLF to simulate long-term power system dynamics.

An example of such long-term dynamics:  A wind ramp causes a governor action response, that in turn affects the area control error (ACE), and is later corrected by automatic generator control (AGC [a.k.a. load frequency control or LFC]). 

Note: Work in progress - everything may be broken.

To install package from current WIP state: "pip install -e ." from this directory

## Current Progress:
* Code refactored to:
    * Utilize Py3<->AMQP<->IPY<-> PSLF workarounds
    * Enable easier code packaging
    * Clarify code structure
    * Unfortunately, AMQP work arounds lead to a slowdown of approx 3-5 times.
    * Non-AMQP code is still functional and will be developed as much as possible in parallel in hopes GE fixes their API (zero breaths held).
* Code creates python mirror of PSLF areas, busses, generators, and loads.
* Various functions have been written to:
  * Check accuracy of mirror
  * Parse .dyd files (more than one)
  * Parse .ltd files
  * Handle H (inertia)
  * Add step and ramp perturbances to loads
  * Distribute changes in Pacc
  * Exectute Combined Swing equation
  * Step dynamic modles (pgov1)
  * Log values of interest
  * Generate data dictionary
  * Import/Export Mirror or data data dictionary as a binary file (via pickle)
  * Export Model or data data dictionary from Python 3.x to MATLAB .mat file
  * Generate terminal output
  * Generate system plots via matplotlib
* MATLAB scripts created to verify simulation outputs of:
  * Combined swing equation to steps in load
  * pgov1 response to steps in load
  * Quick plot (LTDplot) of frequency, P and Q generated, System Loading, and Bus Voltage and Angles.
### Notes:
* To workaround GE API issues: Erlang, RabbitMQ, and Ironpython are required.
* Additional Python packages include:
    * Python 3: Numpy, Scipy, Pika, Matplotlib
    * Ironpython: Pika
* For smaller test cases with only 1 Slack generator, the mirror seems to be 
accurate, however, for the full WECC (with 84 Slack generators), the global
system Slack has yet to be identified programmatically. 
While this will need to be resolved, other issues can be addressed in the meantime.
