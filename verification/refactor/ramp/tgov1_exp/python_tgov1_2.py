# rework so that it takes one time step and compiles
# output similar to how simulation is running

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import scipy.io as sio

Mbase = 100
Pmech = 50
ts = 0.5
# Simulation Parameters
t =np.arange(0,120,ts)#[0,  ts] # 
R = 0.05
Vmax = 1.0*Mbase
Vmin = 0.0
T1 = 0.5
T2 = 3.0
T3 = 10.0
Dt = 0.0

# Inputs
Pref = Pmech*R       # will be a PU of Pref from Generator
delta_w = 0.00

# System Creations
sys1 = sig.StateSpace([-1.0/T1],[1.0/T1],[1.0],0.0)
sys2 = sig.StateSpace([-1.0/T3],[1.0/T3],[1-T2/T3],[T2/T3])

# Input to system
PrefVec = np.array([Pref]*len(t))
dwVec = np.array([delta_w]*len(t))

# add pert
#  to dwV
dwVec[4:100] = 0.70

uVector = (PrefVec-dwVec)/R

# First Block
tout1, y1, x1 = sig.lsim2(sys1, U=uVector, T=t, X0=Pmech)
ys = y1

# limit Valve position
for x in range(ys.size):
    if ys[x]>Vmax:
        ys[x] = Vmax
    elif ys[x]<Vmin:
        ys[x] = Vmin

# Second block
tout2, y2, x2 = sig.lsim2(sys2, ys, t, Pmech)

# Addition of damping
Pmech = y2 - dwVec*Dt

print('Close Plot...')
# Plot Datas
plt.plot(t,x1, label="Valve Position")
plt.plot(t,uVector, label="U Input")
plt.plot(t,Pmech, label="Pmech Out")

plt.title('SciPy Simulated Tgov1')
plt.ylabel(r'$P_{mech}$ [PU]')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.show()

# Output data dictionary as .mat
#pyTgov = {'t_py': t,
#          'y_py': y2,
#          }

#sio.savemat('tgovTest', pyTgov)