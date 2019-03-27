import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import scipy.io as sio

# Inputs:
Pm = .5
Pref = .5 # will be a PU of Pref from Generator
delta_w = 0.0
Sbase = 100

# Initialization parameters
t = np.linspace(0,30,101)

R = 0.05
Vmax = 1.0
Vmin = 0.0
T1 = 0.5
T2 = 3.0
T3 = 10.0
Dt = 0.0

sys1 = sig.TransferFunction(1,[T1, 1])
sys2 = sig.TransferFunction([T2, 1],[T3, 1])

# Input
u = (Pref-delta_w)/R

# First Block
_, y1, x1 = sig.lsim2(sys1, [u]*t.size, t)

# limit between Vmax
for x in range(t.size):
    if y1[x]>Vmax:
        y1[x] = Vmax
    elif y1[x]<Vmin:
        y1[x] =Vmin

# second block
_, y2, x2 = sig.lsim2(sys2, y1,t)

# addition of delta_w*Dt

y2 = y2 + [delta_w*Dt]*y2.size

# Output is Pmech (as PU
plt.plot(t,y2)
plt.grid()
plt.show()
pyTgov = {'t_py': t,
          'y_py': y2,
          }

sio.savemat('tgovTest', pyTgov)