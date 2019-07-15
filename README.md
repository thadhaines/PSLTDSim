# PSLTDSim = Power System Long-Term Dynamic Simulator
Purpose:  Use Python 3 and PSLF to simulate long-term power system dynamics.

Examples of long-term dynamics:  
1. A 20 minute wind ramp causes a governor action response that in turn affects the area control error (ACE), and is later corrected by automatic generator control (AGC [a.k.a. load frequency control or LFC]). 
1. A Generator is tripped in an area that is importing power. Governor action from other areas will respond before AGC works to restore tie-line balance.

Warning: Work in progress - everything may be broken. Nothing guaranteed.

To install package from current WIP state: "pip install -e ." from this directory with administrative privleges.
If python 3 32 bit is not default python: "py -3-32 -m pip install -e ."
Requires IronPython (32 bit) to be on system path.

## What this code does:
  -Uses an agent-based approach to power system modeling.
  -Creates a time sequence of power flows while accounting for combined system frequency, all generator mechanical powers and associated staes, and balancing authority ACE.
  -Uses the PSLF system model format and power flow solver.
  -Communicates with PSLF via Ironpython.
  -Reads PSLF dyd files and creates python equivalents of one governor (tgov1).

## What this code doesn't do:
  -Implement a generic governor for models that are not fully created in Python (i.e. anything besides tgov1).
  -Use definite time controllers to change the status of agents in the system according to user programmable logic.
  -Handle tripping of any generator (power-flow solution diverges).

## Notes:
* To workaround GE API issues: Erlang, RabbitMQ, and Ironpython are required.
* Additional Python packages include:
    * Python 3: Numpy, Scipy, Pika, Matplotlib
    * Ironpython: Pika (Ironpython must be 32 bit to work with GE PSLF middleware)

### Recent Progress:
* Code refactored to:
    * Utilize Py3<->AMQP<->IPY<-> PSLF workarounds
    * Allow for generic automation using agent current value dictionaries
    * Enable easier code packaging
    * Clarify code structure
* Code creates python mirror of PSLF areas, buses, generators, loads, branch sections, and shunts.
* Various functions have been written to:
  * Check accuracy of mirror
  * Parse .dyd files (more than one)
  * Parse .ltd files
  * Handle H (inertia)
  * Add step and ramp perturbances to loads
  * Distribute changes in Pacc
  * Exectute Combined Swing equation
  * Step dynamic modles (tgov1)
  * Log values of interest
  * Generate data dictionary
  * Import/Export Mirror or data data dictionary as a binary file (via sh)
  * Export Model or data data dictionary from Python 3.x to MATLAB .mat file
  * Generate terminal output
  * Generate system plots via matplotlib
* MATLAB scripts created to verify and validate simulation outputs
  * Frequency, Pe, Pm, Q, and Voltage Magnitude and Angle compared to PSDS.
  * Accounts for loss of system inertia and change in system losses.
