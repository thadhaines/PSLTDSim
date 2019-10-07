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

# Knowns
R = 0.05
db = 0.036    # deadband [Hz]
fBase = 60.0
dbPu = db/fBase
dbPu2 = db/2/fBase # Reduced deadband
alpha = dbPu*.7   # Start of deadband
beta = dbPu*1.4 # return to original R

# Shifted deadband calc
R2 = R-dbPu2

# 'Compount R' Calc
# crosses original slope line at beta
R3 = -(alpha-beta)/(beta/R)

# beta where A1 = A2... seems unusable
beta2 = np.roots([1, -alpha, -.5*db**2, .5*(db**2*alpha-(1/R)**2)])

## Agent testing

BAdict0 = {
    'GovDeadbandType' : 'none',
    'GovDeadband' : 0.036, # Hz
    'GovAlpha' : 0.016, #Hz
    'GovBeta' : 0.048, #Hz
    }
BAdict1 = {
    'GovDeadbandType' : 'step',
    'GovDeadband' : 0.036, # Hz
    'GovAlpha' : 0.016, #Hz
    'GovBeta' : 0.048, #Hz
    }
BAdict2 = {
    'GovDeadbandType' : 'ramp',
    'GovDeadband' : 0.018, # Hz
    'GovAlpha' : 0.016, #Hz
    'GovBeta' : 0.048, #Hz
    }
BAdict3 = {
    'GovDeadbandType' : 'NLDroop',
    'GovDeadband' : 0.036, # Hz
    'GovAlpha' : 0.0252, #Hz
    'GovBeta' : 0.0504, #Hz
    }

govDBAgent0 = ltd.filterAgents.deadBandAgent(fBase, R, BAdict0)
govDBAgent1 = ltd.filterAgents.deadBandAgent(fBase, R, BAdict1)
govDBAgent2 = ltd.filterAgents.deadBandAgent(fBase, R, BAdict2)
govDBAgent3 = ltd.filterAgents.deadBandAgent(fBase, R, BAdict3)

# Simulation Vars
fRange = np.arange((1-4*dbPu),(1+4*dbPu),dbPu/25.0) 
u = np.zeros_like(fRange)
u0 = np.zeros_like(fRange)
u1 = np.zeros_like(fRange)
u2 = np.zeros_like(fRange)
r =np.zeros_like(fRange)
r1 =np.zeros_like(fRange)

ndx = 0

for f in fRange:
    delta_w = 1.0-f

    u0[ndx], _ = govDBAgent0.step(delta_w)
    u[ndx], _ = govDBAgent1.step(delta_w)
    u1[ndx], r1[ndx] = govDBAgent2.step(delta_w)
    u2[ndx], r[ndx] = govDBAgent3.step(delta_w)

    """
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
    """

    ndx += 1

#print(fRange)
#print(u)

# Testing of output (i.e input to gain of Mbase and sum pref)
plt.plot(fRange*fBase, u/R, label =r'Step Deadband ($db_1$)')
plt.plot(fRange*fBase, u0/R,ls='--', label =r'No Deadband')
plt.plot(fRange*fBase, u2/r, label =r'Compound R Deadband ($\alpha, \beta$)')
plt.plot(fRange*fBase, u1/r1,ls=':', label =r'Ramp Deadband ($db_2$)')
plt.annotate(r'$\alpha$', xy=((1+alpha)*fBase, 0.005), xytext=((1+alpha)*fBase, -.025),
             arrowprops=dict(facecolor='black', arrowstyle='-'),
             horizontalalignment='center'
             )
plt.annotate(r'$\beta$', xy=((1+beta)*fBase, 0.005), xytext=((1+beta)*fBase, -.025),
             arrowprops=dict(facecolor='black', arrowstyle='-'),
             horizontalalignment='center'
             )
plt.annotate(r'$db_1$', xy=((60+db), 0.005 ), xytext=((60+db), -.025),
             arrowprops=dict(facecolor='black', arrowstyle='-'),
             horizontalalignment='center'
             )
plt.annotate(r'$db_2$', xy=((1+dbPu2)*fBase, 0.005), xytext=((1+dbPu2)*fBase, -.025),
             arrowprops=dict(facecolor='black', arrowstyle='-'),
             horizontalalignment='center'
             )

x1 = fBase-2*db
x2 = fBase+2*db
plt.xlim(x1, x2)
plt.ylim(-.04,.04)
plt.grid(True)
plt.title('Comparison of Deadband Options')
plt.xlabel('Frequency [Hz]')
plt.ylabel('% MW Change')
plt.legend()
plt.show(block = True)
