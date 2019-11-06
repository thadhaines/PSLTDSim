""" Attempt at deadband algorithm and plot """
import matplotlib.pyplot as plt
import numpy as np
import psltdsim as ltd

# For agent use:
# init input: (mirror, parentAgent) dbtype, db, alpha, beta. 
# Checks BAdict for settings, calculates r3
# step input: delta_w (R can be found via attached parentAgent)
# step output delta_w Reff

# 10/6/19 - modified to use agents for testing.
# 10/7/19   Adjusted to make just make plots

# Knowns
R = 0.05
db = 0.036    # deadband [Hz]
fBase = 60.0
dbPu = db/fBase
dbPu2 = .0166/fBase # Reduced deadband
alpha = dbPu2   # Start of deadband
beta = dbPu # return to original R

# Shifted deadband calc
R2 = R-dbPu2

# 'Compount R' Calc
# crosses original slope line at beta
R3 = -(alpha-beta)/(beta/R)

# beta where A1 = A2... seems unusable
beta2 = np.roots([1, -alpha, -.5*db**2, .5*(db**2*alpha-(1/R)**2)])


# Simulation Vars
fRange = np.arange((1-4*dbPu),(1+4*dbPu),dbPu/50.0) 
u = np.zeros_like(fRange)
u0 = np.zeros_like(fRange)
u1 = np.zeros_like(fRange)
u2 = np.zeros_like(fRange)
r =np.zeros_like(fRange)
r1 =np.zeros_like(fRange)

ndx = 0

for f in fRange:
    delta_w = 1.0-f

    ## No Deadband
    u0[ndx] = delta_w

    ## Step deadband
    if abs(delta_w) < (db/fBase):
        delta_w = 0

    u[ndx] = delta_w

    ## Shifted Deadband
    delta_w2 = 1.0-f
    # simple step deadband
    if abs(delta_w2) <= (dbPu2):
        delta_w2 = 0
    # Shift the w to edge of deadband
    elif f < 1:
        delta_w2 -= dbPu2
    else:
        delta_w2 += dbPu2

    u1[ndx]= delta_w2

    ## Compound R
    delta_w3 = 1.0-f
    # standard deadband using alpha as db limit
    if abs(delta_w3) <= (alpha):
        delta_w3 = 0
        r[ndx] = R
    # Shift the w to edge of deadband if less than beta, select R
    else:
        if f<1 and abs(delta_w3) < beta:
            delta_w3 -= alpha
            r[ndx] = R3
        elif f>1 and abs(delta_w3) < beta:
            delta_w3 += alpha
            r[ndx] = R3
        else:
            r[ndx] = R

    # Note: w and r un-altered if past beta
    u2[ndx]= delta_w3

    ndx += 1

#print(fRange)
#print(u)
fig, ax = plt.subplots()
# Testing of output (i.e input to gain of Mbase and sum pref)
ax.plot(fRange*fBase, u0/R,ls='-', label =r'No Deadband', color =[0, 0, 0])
ax.plot(fRange*fBase, u/R, ls='--', label =r'Step Deadband ($db_1$)', color =[.7,.7,.7])
ax.plot(fRange*fBase, u1/R2,ls=':', label =r'No-Step Deadband ($db_2$)', color =[0,1,0])
ax.plot(fRange*fBase, u2/r, ls='-.', label =r'Non-Linear Droop Deadband ($\alpha, \beta$)', color =[1,0,1])

#plt.plot(fRange*fBase, u1/R2,ls=':', label =r'Ramp Deadband ($db_2$)')
ax.annotate(r'$\alpha$', xy=((1+alpha)*fBase, 0.005), xytext=((1+alpha)*fBase, -.018),
             arrowprops=dict(color=[0, 0, 0, 0.25], arrowstyle='-'),
             horizontalalignment='center'
             )
ax.annotate(r'$\beta$', xy=((1+beta)*fBase, 0.005), xytext=((1+beta)*fBase, -.018),
             arrowprops=dict(color=[0, 0, 0, 0.25], arrowstyle='-'),
             horizontalalignment='center'
             )
ax.annotate(r'$db_1$', xy=((60-db), -0.005 ), xytext=((60-db), .018),
             arrowprops=dict(color=[0, 0, 0, 0.25], arrowstyle='-'),
             horizontalalignment='center'
             )
ax.annotate(r'$db_2$', xy=((1-alpha)*fBase, -0.005 ), xytext=((1-alpha)*fBase, .018),
             arrowprops=dict(color=[0, 0, 0, 0.25], arrowstyle='-'),
             horizontalalignment='center'
             )

x1 = fBase-2*db
x2 = fBase+2*db
plt.xlim(x1, x2)
plt.ylim(-.025,.025)
plt.grid(True)
plt.title('Comparison of Deadband Options')
plt.xlabel('Frequency [Hz]')
plt.ylabel(r'PU MW Change [$M_{Base}]$')
plt.legend()

fig.set_dpi(150)
fig.set_size_inches(9*.7, 4.5*.85)
fig.tight_layout()
printFigs = True
if printFigs: plt.savefig('db.pdf', dpi=300)
plt.show(block = True)
plt.pause(0.00001)

