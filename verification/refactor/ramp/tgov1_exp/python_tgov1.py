import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

# Inputs:
Pm = .5
Pref = .5 # will be a PU of Pref from Generator
delta_w = 0.0
Sbase = 100

# Initialization parameters
ts = .5

t = [0, ts] # maybe not needed?

R = 0.05
Vmax = 1.0
Vmin = 0.0
T1 = 0.5
T2 = 3.0
T3 = 10.0
Dt = 0.0

sys1 = sig.TransferFunction(1,[T1, 1]) # 
sys2 = sig.TransferFunction([T2, 1],[T3, 1]) # 


# first block
# input (Pref-delta_w)/R
u = (Pref-delta_w)
print("input: \t\t%.2f" % u)

t1, y1, x1 = sig.lsim2(sys1, [ u, u],[0,ts], Pm)
print('x1 state:\t%f\t%f' %(x1[0],x1[1]))
print('lsim2 y1 out:\t' , end="")
print(y1)

# limit between Vmax
for x in range(2):
    if y1[x]>1.0:
        y1[x] = 1.0
    elif y1[x]<0.0:
        y1[x] =0.0
print('y1 Post Limit:\t' , end="")     
print(y1)

# second block
t2, y2, x2 = sig.lsim2(sys2, [y1[0],y1[1]],[0,ts], Pm)
print('\nlsim2 y2 out:\t' , end="")
print(y2)
print('x2 state:\t%f\t%f' %(x2[0],x2[1]))

# addition of delta_w*Dt

# Output is Pmech (as PU
