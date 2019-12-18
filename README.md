# PSLTDSim = Power System Long-Term Dynamic Simulator
Purpose:  Use Python and PSLF to simulate long-term power system dynamics.

Examples of long-term dynamics:  
1. A 20 minute wind ramp that forces a governor action response that in turn affects the area control error (ACE) which is later corrected by automatic generator control (AGC [a.k.a. load frequency control or LFC]). 
2. A Generator is tripped in an area that is importing power. Governor action from other areas will respond before AGC works to restore tie-line balance.
3. A multi-hour simulation of a daily load cycle and forcast used to assure AGC algorithm operates within NERC mandates.

Warning: Work in progress - everything may be broken. Nothing guaranteed.

To install package from git repository: "pip install -e ." from this directory with administrative privleges.
If python 3 32 bit is not default python: "py -3-32 -m pip install -e ."
Requires IronPython (32 bit) to be on system path.

## What this code does:
  -Uses an agent-based approach to power system modeling.
  
  -Creates a time sequence of power flows while accounting for combined system frequency, all generator mechanical powers and associated staes along with balancing authority states.
  
  -Uses the PSLF system model format and power flow solver.
  
  -Communicates with PSLF via Ironpython.

  -Python 3 communicates with Ironpython via AMQP.
  
  -Reads PSLF dyd files and creates python equivalents of one governor (tgov1).

  -Implements a generic governor for models that are not fully created in Python (i.e. anything besides tgov1).

  -Allows for noise, step, and ramp type perturbances

## What this code doesn't do:

  -Use definite time controllers to change the status of agents in the system according to user programmable logic.
  
  -Handle tripping of any generator (power-flow solution mysteriously diverges).

## Notes:
* Requires GE PSLF Python API and valid PSLF licencse. (sorry)
* To workaround GE API issues: Erlang, RabbitMQ, and Ironpython are required.
* Additional Python packages include:
    * Python 3: Scipy ( for Numpy and Matplotlib) and Pika (for AMQP)
    * Ironpython 2.7 32 bit: Pika (Note: Ironpython must be 32 bit to work with GE PSLF middleware)

### Recent Progress:
* Code refactored to:
    * Utilize Py3<->AMQP<->IPY<-> PSLF workarounds
    * Allow for generic automation using agent current value dictionaries
    * Enable easier code packaging
    * Clarify code structure
* Code creates python mirror of PSLF areas, buses, generators, loads, branch sections, and shunts.
* Code has been written to:
  * Check accuracy of mirror
  * Ignore islanded objects
  * Allow for optional Vsched or Vinit of bus Voltage setting
  * Parse .dyd files (more than one)
  * Parse .ltd files
  * Handle H (inertia)
  * Add noise, step, and ramp perturbances to most any agent value
  * Set area wide governor deadbands
  * Incorporate balancing authority actions into simulation
  * Parse EIA data for multi-hour demand/forcast simulation
  * Distribute changes in Pacc according to inertia
  * Exectute Combined Swing equation
  * Step dynamic modles (tgov1 and genericGov)
  * Log values of interest
  * Generate data dictionary
  * Import/Export Mirror or data data dictionary via shelve
  * Export Model or data data dictionary from Python 3.x to MATLAB .mat file
  * Generate terminal output
  * Generate plots via matplotlib
  * Run multiple simulations in a batch style and handle errors in a non-show stopping way
* MATLAB scripts created to verify and validate simulation outputs
  * Frequency, Pe, Pm, Q, and Voltage Magnitude and Angle compared to PSDS.
  * Branch power flow of P, Q, and I.
  * Accounts for loss of system inertia and change in system losses.
